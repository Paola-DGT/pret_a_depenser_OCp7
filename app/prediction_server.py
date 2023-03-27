"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods, R0801

import logging
from logging.config import dictConfig
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier

from app import ml_tools
from app.settings import log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

app = FastAPI(debug=True)


class Customer(BaseModel):
    """Representation of the data sent by the form with some checks
    that are difficult to be performed by streamlit.
    """

    SK_ID_CURR: float
    FLAG_OWN_CAR: float
    FLAG_OWN_REALTY: float
    CNT_CHILDREN: float
    AMT_INCOME_TOTAL: float
    AMT_CREDIT: float
    AMT_ANNUITY: float
    EXT_SOURCE_1: float
    DAYS_BIRTH: float
    ANNUITY_INCOME_PERC: float
    DAYS_EMPLOYED_PERC: float
    INCOME_CREDIT_PERC: float
    PAYMENT_RATE: float
    TARGET: Optional[float] = np.nan

    def to_pandas(self):
        """Transform class to pandas dataframe."""
        return pd.DataFrame(self.dict(), index=[0])


MODEL: Optional[RandomForestClassifier] = None
CUSTOMER: Optional[Customer] = None


def verify_model():
    """Verifies model exists and is trained."""
    global MODEL
    if not MODEL:
        MODEL = ml_tools.train_and_return()


def predict_risk(data: pd.DataFrame):
    """Makes a prediction from the imputed data."""

    verify_model()
    data = ml_tools.prepare_predict_data(data)

    try:
        logger.info("Running predict function with data: %s", data)
        prediction = MODEL.predict_proba(data)

        return prediction[0][1]

    except Exception as exception:
        raise HTTPException(418, f"Failed to predict {exception}") from exception


@app.post("/make_prediction")
async def calculate_risk(form_request: Customer):
    """Prepares data from user and gets a prediction."""
    global CUSTOMER
    CUSTOMER = form_request
    logger.info("Running model with data: %s", CUSTOMER.dict())
    return predict_risk(CUSTOMER.to_pandas())


@app.post("/decision/{target}")
async def save_customer(target: bool):
    """Receives advisor decision and saves customer"""

    if not CUSTOMER:
        raise HTTPException(400, "Cannot save if no prediction was made")

    CUSTOMER.TARGET = target
    try:
        ml_tools.append_new_customer(CUSTOMER)
    except ValueError as error:
        raise HTTPException(400, "Customer ID error") from error
    logger.info("Customer saved , olk =;with data: %s", CUSTOMER.dict())
    return {"Status": "Customer was saved with current values"}


@app.get("/get_feature_importance")
async def get_feature_importance():
    """Calculates and returns feature importance dataframe as json dict.

    http response data should be reconverted to data frame with the function:
    pd.read_json(data, orient='split')
    """

    features = [
        "FLAG_OWN_CAR",
        "FLAG_OWN_REALTY",
        "CNT_CHILDREN",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "EXT_SOURCE_1",
        "DAYS_BIRTH",
        "ANNUITY_INCOME_PERC",
        "DAYS_EMPLOYED_PERC",
        "INCOME_CREDIT_PERC",
        "PAYMENT_RATE",
    ]
    verify_model()
    logger.info("Getting feature importances")
    feature_importance = pd.DataFrame(
        {"feature": features, "importance": MODEL.feature_importances_}
    )

    return feature_importance.to_json(orient="split")


@app.get("/get_accepted_description")
async def get_accepted_description():
    """Gets statistic data for customers with granted credits"""
    if not CUSTOMER:
        raise HTTPException(
            400, "Customer data is not available yet, make a prediction first."
        )
    return ml_tools.get_general_data_description()


@app.get("/get_customer/{customer_id}")
async def get_customer(customer_id: int):
    """Gets customer information if customer id is known."""
    logger.info("Getting customer data")
    data = ml_tools.get_customer(customer_id)
    logger.info("Replying with customer data: %s", data)
    return data

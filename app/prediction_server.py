"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods

import logging
from logging.config import dictConfig
from typing import TYPE_CHECKING, Union

import pandas as pd
import sklearn.ensemble
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import app.ml_tools as ml_tools
from app.settings import log_conf

if TYPE_CHECKING:
    from pandas import DataFrame
    from sklearn.ensemble import RandomForestClassifier

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

app = FastAPI(debug=True)


class FormRequest(BaseModel):
    """Representation of the data sent by the form with some checks
    that are difficult to be performed by streamlit.
    """
    # TODO: Add "SK_ID_CURR" to this class and to the dashboard
    FLAG_OWN_CAR: float
    FLAG_OWN_REALTY: float
    CNT_CHILDREN: float
    AMT_CREDIT: float
    AMT_INCOME_TOTAL: float
    EXT_SOURCE_1: float
    DAYS_BIRTH: float
    ANNUITY_INCOME_PERC: float
    DAYS_EMPLOYED_PERC: float
    INCOME_CREDIT_PERC: float
    PAYMENT_RATE: float
    AMT_ANNUITY: float


MODEL: Union[None, RandomForestClassifier] = None


def predict_risk(data: DataFrame):
    """Makes a prediction from the imputed data."""
    global MODEL

    if not MODEL:
        MODEL = ml_tools.train_and_return()

    try:
        logger.info(f"Running predict function with data: {data.to_dict()}")
        prediction = MODEL.predict_proba(data)
        return prediction
    except Exception as exc:
        raise HTTPException(418, "Data provided is untreatable") from exc


@app.post("/make_prediction")
async def calculate_risk(form_request: FormRequest):
    """Prepares data from user and gets a prediction."""
    logger.info("Running model with data: %s", form_request.dict())
    # TODO: when "SK_ID_CURR" will be added you have to prepare_predict_data here
    #   and pass it to the predict_risk
    data = pd.DataFrame(form_request.dict(), index=[0])
    return predict_risk(data) # TODO: check type and format of data returned

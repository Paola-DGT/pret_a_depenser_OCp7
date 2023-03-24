"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods

import logging
from logging.config import dictConfig

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app import ml_tools
from app.settings import log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

app = FastAPI(debug=True)


class FormRequest(BaseModel):
    """Representation of the data sent by the form with some checks
    that are difficult to be performed by streamlit.
    """

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


MODEL = None


def predict_risk(data: pd.DataFrame):
    """Makes a prediction from the imputed data."""
    global MODEL

    if not MODEL:
        MODEL = ml_tools.train_and_return()

    try:
        logger.info("Running predict function with data: %s", data)
        prediction = MODEL.predict_proba(data)
        return prediction[0][1]
    except Exception as exception:
        raise HTTPException(418, f"Failed to predict {exception}") from exception


@app.post("/make_prediction")
async def calculate_risk(form_request: FormRequest):
    """Prepares data from user and gets a prediction."""
    logger.info("Running model with data: %s", form_request.dict())
    data = pd.DataFrame(form_request.dict(), index=[0])
    return predict_risk(data)  # TODO: check type and format of data returned

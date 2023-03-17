"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods

import logging
from logging.config import dictConfig
from typing import Union

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pandas import DataFrame
from pydantic import BaseModel

from app.settings import conf, log_conf

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
    AMT_CREDIT: float
    AMT_INCOME_TOTAL: float
    EXT_SOURCE_1: float
    DAYS_BIRTH: float
    ANNUITY_INCOME_PERC: float
    DAYS_EMPLOYED_PERC: float
    INCOME_CREDIT_PERC: float
    PAYMENT_RATE: float
    AMT_ANNUITY: float


def predict_risk(data: DataFrame):
    """Calls the mlflow prediction module with the given model."""
    mlflow.set_tracking_uri(conf.MLFLOW_URL)

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(conf.LOGGED_MODEL)
    logger.info("Running model: %s", loaded_model)

    # Predict on a Pandas DataFrame.
    try:
        logger.info("Running predict function")
        result = loaded_model.predict(pd.DataFrame(data))
        logger.info("result: %s", result)
        return result
    except Exception as exc:
        raise HTTPException(418, "Data provided is untreatable") from exc


@app.post("/make_prediction")
async def calculate_risk(form_request: FormRequest):
    """Prepares data from user and gets a prediction."""
    logger.info("Running model with data: %s", form_request.dict())
    data = pd.DataFrame(form_request.dict(), index=[0])
    return predict_risk(data)[0]

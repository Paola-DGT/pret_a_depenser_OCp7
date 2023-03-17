"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods

import logging
from typing import Union

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pandas import DataFrame
from pydantic import BaseModel

from app.settings import conf

logger = logging.getLogger(__name__)
app = FastAPI()


class FormRequest(BaseModel):
    """Representation of the data sent by the form with some checks
    that are difficult to be performed by streamlit.
    """

    # name: str
    # lastname: str
    # age: int
    # annual_income: int
    # intended_credit: int
    # marital_status: str
    # number_of_children: Optional[int]

    # @validator("age")
    # # pylint: disable=no-self-argument
    # def check_age(cls, age: int) -> int:
    #     """Verifies thage of applicant."""
    #     if 19 < age > 70:
    #         raise ValueError("Age is off applicant accepted age policy")
    #     return age
    #
    # @validator("name", "lastname")
    # def check_name(cls, name: str) -> str:
    #     """Verifies name and lastname are only alpha chars."""
    #     re.compile(r"^[a-zA-Z]+$")
    #     if not re.match(name):
    #         raise ValueError(f"{name} contains invalid characters")
    #     return name
    FLAG_OWN_CAR: bool
    FLAG_OWN_REALTY: bool
    CNT_CHILDREN: int
    AMT_CREDIT: Union[float, int]
    AMT_INCOME_TOTAL: Union[float, int]
    EXT_SOURCE_1: Union[float, int]
    DAYS_BIRTH: int
    ANNUITY_INCOME_PERC: float
    DAYS_EMPLOYED_PERC: float
    INCOME_CREDIT_PERC: float
    PAYMENT_RATE: Union[float, int]
    AMT_ANNUITY: Union[float, int]


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

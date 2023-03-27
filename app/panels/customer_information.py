"""This is the dashboard customer form module, contains all the fields necessary
to obtain a risk prediction.
"""
from __future__ import annotations

# pylint: disable=R0801
import datetime
import json
import logging
from dataclasses import asdict, dataclass
from logging.config import dictConfig
from typing import Optional, Union

import requests
import streamlit as st

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")


@dataclass(order=True)
class Customer:
    """Representation of customer data handled on front."""

    # pylint: disable=invalid-name, R0902
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
    TARGET: Optional[float]


def get_yes_no_resp(text: str, key: str, value: int):
    """Change yes/no to boolean"""

    has_car = st.selectbox(f"{text}", ["no", "yes"], key=key, index=value)
    return 0 if has_car == "yes" else 1


CAP4_HELP = """Total years worked \n
e.g: 2.5years (2years and 6 months)
"""


def work_percentage(days_b: int):
    """Operation por obtenir le percentage"""
    working_years = st.number_input(
        "Years worked", value=1, min_value=1, help=CAP4_HELP
    )
    working_days = working_years * 365
    percentage = abs(days_b) / working_days
    return percentage


CAP_HELP = """Annual paymentof the requested loan\n
e.g.: 1500 (fifteen hundred)
"""
CAP2_HELP = """Annual salary\n
e.g.: 35000(thirty-five thousand)
"""


def annuity_percentage(
    anuity: float, income: float
) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    """calcul annuity percentage"""
    amt_annuity = st.number_input(
        "Credit annuity payment", min_value=1, help=CAP_HELP, value=int(anuity)
    )
    amt_income_total = st.number_input(
        "Yearly Income", min_value=1, help=CAP2_HELP, value=int(income)
    )
    annuity_percent = amt_annuity / amt_income_total
    return amt_annuity, amt_income_total, annuity_percent


CAP3_HELP = """Amount of loan demanded\n
e.g.:7000 (seven thousand)
"""


def income_credit_percentage(
    amt_income_total: float, credit_value: float
) -> tuple[Union[int, float], float]:
    """calcul income/credit percentage"""
    amt_credit = st.number_input(
        "Credit Demand", min_value=1, help=CAP2_HELP, value=int(credit_value)
    )
    income_credit = amt_income_total / amt_credit
    return amt_credit, income_credit


def days_birth() -> int:
    """Change birthday(date) to days(chiffre)"""
    birth_date = st.date_input(
        "Birthday",
        value=datetime.date(2004, 1, 1),
        min_value=datetime.date(1948, 1, 1),
        max_value=datetime.date(2005, 1, 1),
    )
    current_day = datetime.datetime.now().date()
    delta = current_day - birth_date
    return -delta.days


# pylint: disable=inconsistent-return-statements
def dashboard() -> tuple[Optional[float], Customer]:
    """Main dashboard code."""

    customer_id = st.number_input("Client number", min_value=100000)
    temp_customer: Optional[Customer] = None

    if st.button("Get Customer"):
        logger.info("requesting previous client, client id: %s", customer_id)
        result = requests.request(
            method="GET",
            url="".join([conf.GET_CUSTOMER, "/", str(customer_id)]),
            headers={"content-type": "application/json"},
            timeout=360,
        )
        logger.info("got customer raw info as: %s", json.loads(result.content.decode()))

        if result.status_code == 200:
            customer = json.loads(result.content.decode())[-1]
            temp_customer = Customer(**customer)
            logger.info("Got customer as: %s", asdict(temp_customer))
            st.success(
                f"Customer previous application status is: "
                f"{'accepted' if temp_customer.TARGET == 0 else 'rejected'}"
            )
        else:
            logger.error("The request failed: %s")
            st.error(f"Customer {customer_id} not found")

    has_car = temp_customer.FLAG_OWN_CAR if temp_customer else 0
    has_realty = temp_customer.FLAG_OWN_REALTY if temp_customer else 0
    cnt_child = temp_customer.CNT_CHILDREN if temp_customer else 1
    anuity = temp_customer.AMT_ANNUITY if temp_customer else 1
    income = temp_customer.AMT_INCOME_TOTAL if temp_customer else 1
    credit_demand = temp_customer.AMT_CREDIT if temp_customer else 1
    ext_source = temp_customer.EXT_SOURCE_1 if temp_customer else None
    days_birth_temp = temp_customer.DAYS_BIRTH if temp_customer else 1

    days_b = days_birth()
    amt_annuity, amt_income_total, annuity_percent = annuity_percentage(anuity, income)
    amt_credit, income_credit = income_credit_percentage(
        amt_income_total, credit_demand
    )

    customer = Customer(
        SK_ID_CURR=customer_id,
        FLAG_OWN_CAR=get_yes_no_resp("Did you have a car?", "has_car", has_car),
        FLAG_OWN_REALTY=get_yes_no_resp(
            "Did you have an appartement or a house", "has_house", has_realty
        ),
        CNT_CHILDREN=st.number_input(
            "Number of Children", min_value=0, value=cnt_child
        ),
        AMT_INCOME_TOTAL=amt_income_total,
        AMT_CREDIT=amt_credit,
        AMT_ANNUITY=amt_annuity,
        EXT_SOURCE_1=st.number_input(
            "External Source",
            min_value=0.0,
            value=0.5059 if not ext_source else ext_source,
            max_value=1.0,
            format="%4f",
            help="score rating of confidence for the acquisition of credit",
        ),
        DAYS_BIRTH=days_b if not days_birth_temp else days_birth_temp,
        ANNUITY_INCOME_PERC=annuity_percent,
        DAYS_EMPLOYED_PERC=work_percentage(days_b),
        INCOME_CREDIT_PERC=income_credit,
        PAYMENT_RATE=amt_annuity / amt_credit,
        TARGET=None,
    )

    pred = None

    if st.button("Calculate"):
        data = asdict(customer)
        logger.info("Running_dashboard: %s", data)
        result = requests.request(
            method="POST",
            url=conf.PREDICTION_ENDPOINT,
            headers={"content-type": "application/json"},
            json=data,
            timeout=360,
        )

        if result.status_code == 200:
            pred = result.content.decode()
            st.success(f"Score = {pred}.\nYou can go to Customer Analysis Tab")

        return float(pred) if pred else pred, customer

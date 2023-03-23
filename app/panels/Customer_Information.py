"""THis is the dashboard module of the risk prediction app."""

import datetime
import logging
from logging.config import dictConfig

import requests
import streamlit as st

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

st.title("Pret a Depenser")


def get_yes_no_resp(text, key):
    """Change yes/no to boolean"""
    has_car = st.selectbox(f"{text}", ["yes", "no"], key=key)
    return 0 if has_car == "yes" else 1


CAP4_HELP = """Total years worked \n
e.g: 2.5years (2years and 6 months)
"""


def work_percentage(days_b):
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


def annuity_percentage():
    """calcul annuity percentage"""
    amt_annuity = st.number_input("Credit annuity payment", min_value=1, help=CAP_HELP)
    amt_income_total = st.number_input("Yearly Income", min_value=1, help=CAP2_HELP)
    annuity_percent = amt_annuity / amt_income_total
    return amt_annuity, amt_income_total, annuity_percent


CAP3_HELP = """Amount of loan demanded\n
e.g.:7000 (seven thousand)
"""


def income_credit_percentage(amt_income_total):
    """calcul income/credit percentage"""
    amt_credit = st.number_input("Credit Demand", min_value=1, help=CAP2_HELP)
    income_credit = amt_income_total / amt_credit
    return amt_credit, income_credit


def dashboard():
    """Main dashboard code"""

    def days_birth():
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

    st.text(
        """Pret a depenser, offers you a clear, fast and adapted loan to your needs.
        Fill in the questionnaire and find out if you can benefit from a loan or
        financial aid."""
    )

    sk_id_curr = st.number_input("Client number", min_value=1000)

    days_b = days_birth()
    amt_annuity, amt_income_total, annuity_percent = annuity_percentage()
    amt_credit, income_credit = income_credit_percentage(amt_income_total)

    data = {
        "FLAG_OWN_CAR": get_yes_no_resp("Did you have a car?", "has_car"),
        "FLAG_OWN_REALTY": get_yes_no_resp(
            "Did you have an appartement or a house", "has_house"
        ),
        "CNT_CHILDREN": st.number_input("Number of Children", min_value=0),
        "AMT_INCOME_TOTAL": amt_income_total,
        "AMT_CREDIT": amt_credit,
        "EXT_SOURCE_1": st.number_input(
            "External Source",
            min_value=0.0,
            value=0.5059,
            max_value=1.0,
            format="%4f",
            help="score rating of confidence for the acquisition of credit",
        ),
        "DAYS_BIRTH": days_b,
        "ANNUITY_INCOME_PERC": annuity_percent,
        "DAYS_EMPLOYED_PERC": work_percentage(days_b),
        "INCOME_CREDIT_PERC": income_credit,
        "PAYMENT_RATE": amt_annuity / amt_credit,
        "AMT_ANNUITY": amt_annuity,
    }

    pred = None

    if st.button("Calculate"):
        logger.info("Running_dashboard: %s", data)
        result = requests.request(
            method="POST",
            url=conf.PREDICTION_ENDPOINT,
            headers={"content-type": "application/json"},
            json=data,
            timeout=360,
        )

        if result.status_code == 200:
            st.success(f"Score = {result.content.decode()}")
            pred = result.content.decode()

        return pred

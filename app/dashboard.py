"""THis is the dashboard module of the risk prediction app."""

import datetime

import requests
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate

from app.settings import conf


def get_yes_no_resp(text, key):
    """Change yes/no to boolean"""
    has_car = st.selectbox(f"{text}", ["yes", "no"], key=key)
    return 1 if has_car == "yes" else 0


def work_percentage(days_b):
    """Operation por obtenir le percentage"""
    working_years = st.number_input("Years worked", value=1, min_value=1)
    working_days = working_years * 365
    percentage = days_b / working_days
    return percentage


def annuity_percentage():
    """calcul annuity percentage"""
    amt_annuity = st.number_input("Credit annuity payment", min_value=1)
    amt_income_total = st.number_input("Yearly Income", min_value=1)
    annuity_percent = amt_annuity / amt_income_total
    return amt_annuity, amt_income_total, annuity_percent


def income_credit_percentage(amt_income_total):
    """calcul income/credit percentage"""
    amt_credit = st.number_input("Credit Demand", min_value=1)
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
        return delta.days

    st.text(
        """Pret a depenser, vous offre un prêt clair, rapide et adapté à vos besoins.
        Remplissez le questionnaire et découvrez si vous pouvez bénéficier d'un prêt ou
        d'une aide financière."""
    )

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
            "External Source", min_value=0.0, value=0.5059, max_value=1.0, format="%4f"
        ),
        "DAYS_BIRTH": days_b,
        "ANNUITY_INCOME_PERC": annuity_percent,
        "DAYS_EMPLOYED_PERC": work_percentage(days_b),
        "INCOME_CREDIT_PERC": income_credit,
        "PAYMENT_RATE": amt_annuity / amt_credit,
        "AMT_ANNUITY": amt_annuity,
    }

    if st.button("Calculate"):
        result = requests.request(
            method="POST",
            url=conf.PREDICTION_ENDPOINT,
            headers={"content-type": "application/json"},
            json=data,
            timeout=360,
        )

        if result.status_code == 200:
            st.success(f"Score = {result.content.decode()}")


def load_auth() -> Authenticate:
    """Loads authentication file and creates auth obj."""

    with open(conf.AUTH_FILE_PATH, encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator


# Start authentication
authentic = load_auth()


#           PAGE STARTS HERE        #
st.title("Simple Regresion Model")
st.subheader("City-cycle fuel consumption in miles per gallon")

# authentication banner
name, authentication_status, username = authentic.login("Login", "main")

# if is authenticated we show the dashboard
if authentication_status:
    authentic.logout("Logout", "main")
    st.write(f"Welcome *{name}*")
    dashboard()
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

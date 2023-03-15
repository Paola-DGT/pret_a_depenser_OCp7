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


def dashboard():
    """Main dashboard code"""

    st.text(
        """Pret a depenser, vous offre un prêt clair, rapide et adapté à vos besoins.
        Remplissez le questionnaire et découvrez si vous pouvez bénéficier d'un prêt ou
        d'une aide financière."""
    )

    data = {
        "FLAG_OWN_CAR": get_yes_no_resp("Did you have a car?", "has_car"),
        "FLAG_OWN_REALTY": get_yes_no_resp(
            "Did you have an appartement or a house", "has_house"
        ),
        "CNT_CHILDREN": st.number_input("childrens", min_value=0),
        "AMT_INCOME_TOTAL": st.number_input("Income", min_value=10000),
        "AMT_CREDIT": st.number_input("Credit", min_value=10000),
        "EXT_SOURCE_1": st.number_input("External Source", min_value=0),
        "DAYS_BIRTH": days_birth(),
        "ANNUITY_INCOME_PERC": st.number_input(
            "Percentage of income", min_value=0, max_value=1
        ),
        "DAYS_EMPLOYED_PERC": st.number_input(
            "Percentage with a job", min_value=0, max_value=1
        ),
        "INCOME_CREDIT_PERC": st.number_input(
            "Percentage credit/income", min_value=0, max_value=1
        ),
        "PAYMENT_RATE": st.number_input("Payment rate", min_value=0, max_value=1),
        "AMT_ANNUITY": st.number_input("Amount Annuity", min_value=0),
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

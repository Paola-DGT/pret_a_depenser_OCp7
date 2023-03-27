"""Dashboard start page to handle sub pages"""

import logging
from logging.config import dictConfig

import streamlit as st
import yaml
from streamlit_authenticator import Authenticate

from app.panels.costumer_analysis import customer_analysis
from app.panels.customer_information import dashboard
from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("front-app")

CA_FLAG = False
PREDICTION = None
CUSTOMER = None


def start():
    """Start page for dashboard."""

    st.text(
        """Pret a depenser, offers you a clear, fast and adapted loan to your needs.
    Fill in the questionnaire and find out if you can benefit from a loan or
    financial aid."""
    )

    cus_inf, cus_ana = st.tabs(["Customer Information", "Customer Analysis"])

    # if st.button("Customer Info"):
    with cus_inf:
        global PREDICTION, CUSTOMER
        PREDICTION, CUSTOMER = dashboard() or (None, None)

        global CA_FLAG
        CA_FLAG = PREDICTION is not None

    with cus_ana:
        if CA_FLAG:
            customer_analysis(PREDICTION, CUSTOMER)


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


# ______________________________ Page is generated here ____________________________

st.title("Pret a Depenser")
st.subheader("Credit application")

# Start authentication
authentic = load_auth()

name, authentication_status, username = authentic.login("Login", "main")

if authentication_status:
    authentic.logout("Logout", "main")
    st.write(f"Welcome *{name}*")
    start()

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

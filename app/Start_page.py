import json
import logging
from logging.config import dictConfig
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yaml
from streamlit.components.v1 import html
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_authenticator import Authenticate

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")


def start():
    st.text(
        """Pret a depenser, offers you a clear, fast and adapted loan to your needs.
    Fill in the questionnaire and find out if you can benefit from a loan or
    financial aid."""
    )

    cus_inf, cus_ana, maint = st.tabs(
        ["Customer Information", "Customer Analysis", "Maintenance"]
    )

    # if st.button("Customer Info"):
    with cus_inf:
        from panels.Customer_Information import dashboard

        prediction = dashboard()

    with cus_ana:
        from panels.Costumer_Analysis import customer_analysis

        if prediction:
            customer_analysis()

    # if st.button("Maintenance"):
    with maint:
        from panels.Maintenance import maintenance

        maintenance()


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

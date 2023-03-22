import logging
from logging.config import dictConfig

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

st.set_page_config(page_title="Pret a depenser", initial_sidebar_state="collapsed")

st.title("Pret a Depenser")
st.subheader("Credit application")


def start():
    st.text(
        """Pret a depenser, offers you a clear, fast and adapted loan to your needs.
    Fill in the questionnaire and find out if you can benefit from a loan or
    financial aid."""
    )

    if st.button("Customer Info"):
        ...

    if st.button("Maintenance"):
        ...


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

name, authentication_status, username = authentic.login("Login", "main")

if authentication_status:
    authentic.logout("Logout", "main")
    st.write(f"Welcome *{name}*")
    start()
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

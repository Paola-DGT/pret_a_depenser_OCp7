"""THis is the dashboard module of the risk prediction app."""

import requests
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate

from app.settings import conf


def dashboard():
    """Main dashboard code"""

    st.text(
        """Source: This dataset was taken from the StatLib library which is maintained
        at Carnegie Mellon University.
        The dataset was used in the 1983 American Statistical Association Exposition.
    Data Set Information: This dataset is a slightly modified version of the dataset
    provided in the StatLib library.
        In line with the use by Ross Quinlan (1993) in predicting the attribute "mpg",
        8 of the original instances were
        removed because they had unknown values for the "mpg" attribute. The original
        dataset is available in the file
        "auto-mpg.data-original".
    The data concerns city-cycle fuel consumption in miles per gallon, to be predicted
    in terms of 3 multivalued
    discrete and 5 continuous attributes." (Quinlan, 1993) """
    )

    data = {
        "cylinders": st.number_input("cylinders", min_value=1, max_value=16, value=8),
        "displacement": st.number_input(
            "displacement", min_value=150, max_value=1500, value=350
        ),
        "horsepower": st.number_input(
            "horsepower", min_value=45, max_value=900, value=165
        ),
        "weight": st.number_input("weight", min_value=2000, max_value=5000, value=3693),
        "acceleration": st.number_input(
            "acceleration", min_value=2.0, max_value=30.0, value=11.5
        ),
        "model_year": st.number_input(
            "model_year", min_value=10, max_value=99, value=70
        ),
        "origin": st.number_input("origin", min_value=1, max_value=5, value=1),
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

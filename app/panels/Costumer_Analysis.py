import json
import logging
from dataclasses import asdict
from logging.config import dictConfig
from typing import Any

import pandas as pd
import requests
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
from panels.Customer_Information import Customer

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("front-app")


def pred_text(score: float) -> str:
    """Helper to set the score text."""
    if score < 0.3:
        return f"{score} which is very high risk BE CAREFUL !"
    if 0.3 <= score <= 0.5:
        return f"{score} which is high risk CAUTION, Reconsider"
    if 0.5 < score < 0.6:
        return f"{score} which is medium risk, be precautious"
    if 0.6 < score <= 0.8:
        return f"{score} which is low risk, proceed carefully"
    if 0.8 < score <= 1:
        return f"{score} which is very low risk, proceed without problems"


def display_importances(feature_importance_df: pd.DataFrame) -> Any:
    """Builds feature importance graph."""

    feature_importance_df.sort_values(
        by=["importance"],
        ascending=False,
        inplace=True,
        ignore_index=True,
        axis=0,
    )

    st.bar_chart(
        y="importance",
        x="feature",
        data=feature_importance_df,
    )


def get_fi():
    """Gets Feature importance and builds the graph to display"""
    logger.info("Getting Feature Importance")

    result = requests.request(
        method="GET",
        url=conf.GET_FI_ENDPOINT,
        headers={"content-type": "application/json"},
        timeout=360,
    )

    if result.status_code == 200:
        feat_imp = json.loads(result.content.decode())
        logger.info("Got FI as: %s", feat_imp)
        feat_imp = pd.read_json(feat_imp, orient="split")
        display_importances(feat_imp)
    else:
        raise Exception(
            f"Cannot Display Feature Importance Graph code {result.status_code}"
        )


# Custumer analysis
def customer_analysis(score: float, customer: Customer):
    """Main screen of Customer Analysis section."""
    st.subheader("Costumer Analysis")

    st.write(
        f"### Customer {customer.SK_ID_CURR} obtained a score of: {pred_text(score)}"
    )

    get_fi()

    data = asdict(customer)

    st.selectbox("Accepted", ["yes", "no"])
    st.button("save")

import json
import logging
from dataclasses import asdict
from logging.config import dictConfig
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
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


def display_importances(feature_importance_df: pd.DataFrame) -> None:
    """Builds feature importance graph."""

    feature_importance_df.sort_values(
        by=["importance"],
        ascending=False,
        inplace=True,
        ignore_index=True,
        axis=0,
    )

    figure = px.bar(feature_importance_df, x="feature", y="importance")
    st.plotly_chart(figure)


def plot_accepted_vs_current(customer: Customer, accepted: Any) -> None:
    """Plots bar graphs of bolean and radar chart for the others."""
    logger.info("plot funct got type: %s", type(accepted))
    # ________ Radar Data Construction _______
    radar_data = pd.read_json(accepted[0], orient="split")
    customer_df = pd.DataFrame(asdict(customer), index=["customer"])
    customer_df.drop(
        ["FLAG_OWN_CAR", "FLAG_OWN_REALTY", "CNT_CHILDREN", "SK_ID_CURR", "TARGET"],
        axis=1,
        inplace=True,
    )

    radar_data = radar_data.append(customer_df)

    # normalization
    radar_data = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min())

    categories = radar_data.columns

    logger.info("building radar graph with DF:\n %s", radar_data)

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=radar_data.loc["max"].values,
            theta=categories,
            fill="toself",
            fillcolor="grey",
            opacity=0.4,
            marker=dict(color="grey"),
            name="Accepted max",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=radar_data.loc["mean"].values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(0, 0, 255, 0.4)",
            opacity=0.6,
            marker=dict(color="blue"),
            name="Accepted Mean",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=radar_data.loc["customer"].values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(0, 255, 0, 0.4)",
            opacity=0.6,
            marker=dict(color="Green"),
            name="Client situation",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title_text="Customer data compared to the mean and max of all approuved "
        "applications",
    )

    # Display radar chart
    st.plotly_chart(fig)

    # ____________________ Bar Chart Construction _____________________

    bar_data = accepted[1]
    own_car, own_realty, cnt_children = [pd.read_json(data) for data in bar_data]

    mixed_yes_no = own_car.append(own_realty, ignore_index=True)

    fig_mixed = px.bar(
        mixed_yes_no,
        x="index",
        labels={
            "index": "Has item =1, does not has item = 0",
            "data": "Number of accepted customers in database",
        },
        y="data",
        color="name",
        title="Car and Realty tenants among customers with authorized credits",
    )
    fig_mixed.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1))

    fig_children = px.bar(
        cnt_children.iloc[:-5, :],
        x="index",
        labels={
            "index": "Number of children",
            "data": "Number of accepted customers in database",
        },
        y="data",
        title="Number of children per accepted applicant in database",
    )
    fig_children.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1))

    # Show the graphs
    st.plotly_chart(fig_mixed)
    st.plotly_chart(fig_children)


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


def get_accepted_stats(customer: Customer):
    """Gets a describe data frame of the previously accepted customers."""
    logger.info("Getting Accepted Stats")

    result = requests.request(
        method="GET",
        url=conf.GET_ACCEPTED_DESC_ENDPOINT,
        headers={"content-type": "application/json"},
        timeout=360,
    )

    if result.status_code == 200:
        accepted_stats = json.loads(result.content.decode())
        logger.info("Got Accepted stats as: %s", accepted_stats)
        plot_accepted_vs_current(customer, accepted_stats)
    else:
        raise Exception(
            f"Cannot display graph: accepted customers vs current code {result.status_code}"
        )


# Custumer analysis page is built up on this function.
def customer_analysis(score: float, customer: Customer):
    """Main screen of Customer Analysis section."""
    st.subheader("Costumer Analysis")
    st.write(
        f"### Customer {customer.SK_ID_CURR} obtained a score of: {pred_text(score)}"
    )

    # Display feature importances of the model used to make the prediction.
    get_fi()

    # Display position of client relative to the average client wich was accepted.

    get_accepted_stats(customer)

    # data = asdict(customer)

    st.selectbox("Accepted", ["yes", "no"])
    st.button("save")

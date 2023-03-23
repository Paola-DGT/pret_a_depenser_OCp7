import streamlit as st

# import pandas as pd
# import numpy as np

# Costumer analysis
def customer_analysis():
    st.subheader("Costumer Analysis")

    # st.plotly_chart("nombre graph".png)

    st.selectbox("Accepted", ["yes", "no"])
    st.button("save")

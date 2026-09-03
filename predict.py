import streamlit as st
import time
import requests
import pandas as pd
from mlflow_client import MlflowClient


if "mlflow" not in st.session_state:
    mlflow_client = MlflowClient()
    st.session_state.mlflow = mlflow_client
    st.session_state.mlflow_models = mlflow_client.get_registered_models()
mlflow_client = st.session_state.mlflow
mlflow_models = st.session_state.mlflow_models


def render_form(id, uploader_label):
    form = st.form(id, border=False)
    model = form.selectbox(
        "Select a model",
        mlflow_models,
        help="Select the model to use for prediction."
    )
    slider = form.slider("Error tolerance", 0, 100, 5)
    upload = form.file_uploader(uploader_label, type=["csv"])

    # Every form must have a submit button.
    submitted = form.form_submit_button("Submit")
    if submitted:
        # get uploaded data as csv
        if upload is not None:
            data = pd.read_csv(upload, index_col=0)
            predictions = mlflow_client.predict(model, data, slider)
            st.write(predictions)
        else:
            st.error("Please upload a file.")


gex_tab, dnam_tab = st.tabs(["Gene Expresssion", "DNA Methylation"])
with gex_tab:
    render_form("gex_form", "Gene expression data")
with dnam_tab:
    render_form("dnam_form", "DNA methylation data")

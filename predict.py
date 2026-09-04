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

# Order models as follows: all models containing "latest" first
mlflow_models = sorted(mlflow_models, key=lambda x: "latest" in x, reverse=True)


def render_form(id, uploader_label):
    form = st.form(id, border=False)
    model = form.selectbox(
        "Select a model",
        mlflow_models,
        help="Select the model to use for prediction."
    )
    slider = form.slider("Error tolerance", 0, 100, 5)
    upload = form.file_uploader(uploader_label, type=["csv"])
    labels_upload = form.file_uploader(
        "If subtypes are known, upload labels (optional)", type=["csv"])

    # Every form must have a submit button.
    submitted = form.form_submit_button("Submit")
    if submitted:
        # get uploaded data as csv
        if upload is not None:
            data = pd.read_csv(upload, index_col=0)
            labels = None
            if labels_upload is not None:
                labels = pd.read_csv(labels_upload, index_col=0)
            predictions = mlflow_client.predict(model, data, slider, labels=labels)
            st.write(predictions)
        else:
            st.error("Please upload a file.")


render_form("prediction_form", "MLOmix-processed GEX or DNAm data")

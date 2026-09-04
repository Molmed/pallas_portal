import streamlit as st
import pandas as pd
from mlflow_client import MlflowClient
import matplotlib.pyplot as plt
from upsetplot import plot


st.set_page_config(
    page_title="PALLAS Predictions",
    layout="wide",
)

if "mlflow" not in st.session_state:
    mlflow_client = MlflowClient()
    st.session_state.mlflow = mlflow_client
    st.session_state.mlflow_models = mlflow_client.get_registered_models()
mlflow_client = st.session_state.mlflow
mlflow_models = st.session_state.mlflow_models

# Order models as follows: all models containing "latest" first
mlflow_models = sorted(mlflow_models, key=lambda x: "latest" in x, reverse=True)


def upset_plot(predictions, color="#9768ac"):
    raw_predictions = predictions["prediction"].tolist()

    prediction_sets = [
        set(value) if isinstance(value, (list, tuple, set, frozenset))
        else {value}
        for value in raw_predictions
    ]

    class_names = sorted(
        {label for values in prediction_sets for label in values},
        key=str,
    )

    if not class_names:
        st.info("No prediction classes available to plot.")
        return

    upset_data = pd.DataFrame(
        [
            {class_name: class_name in values for class_name in class_names}
            for values in prediction_sets
        ],
        dtype=bool,
    )

    upset_data = upset_data.loc[:, upset_data.any(axis=0)]
    upset_data.set_index(upset_data.columns.tolist(), inplace=True)

    fig = plt.figure()
    plt.rcParams['font.size'] = 8
    plot(
        upset_data,
        fig=fig,
        element_size=25,
        sort_by="cardinality",
        facecolor=color,
        show_counts="%d",
        show_percentages=False
    )
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


def render_form(form_id, uploader_label):
    form_column, output_column = st.columns([1, 2], gap="large")

    with form_column:
        with st.form(form_id, border=False):
            model = st.selectbox(
                "Select a model",
                mlflow_models,
                help="Select the model to use for prediction.",
            )
            slider = st.slider("Error tolerance", 0, 100, 5)
            upload = st.file_uploader(uploader_label, type=["csv"])
            labels_upload = st.file_uploader(
                "If subtypes are known, upload labels (optional)",
                type=["csv"],
            )
            submitted = st.form_submit_button("Submit")

    with output_column:
        if not submitted:
            return

        if upload is None:
            st.error("Please upload a file.")
            return

        data = pd.read_csv(upload, index_col=0)
        labels = (
            pd.read_csv(labels_upload, index_col=0)
            if labels_upload is not None
            else None
        )

        predictions = mlflow_client.predict(
            model,
            data,
            slider,
            labels=labels,
        )

        st.write(predictions)
        upset_plot(predictions)


render_form("prediction_form", "MLOmix-processed GEX or DNAm data")

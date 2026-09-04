import streamlit as st
import pandas as pd
from mlflow_client import MlflowClient
import matplotlib.pyplot as plt
from upsetplot import plot


if "mlflow" not in st.session_state:
    mlflow_client = MlflowClient()
    st.session_state.mlflow = mlflow_client
    st.session_state.mlflow_models = mlflow_client.get_registered_models()
mlflow_client = st.session_state.mlflow
mlflow_models = st.session_state.mlflow_models

# Order models as follows: all models containing "latest" first
mlflow_models = sorted(mlflow_models, key=lambda x: "latest" in x, reverse=True)


def upset_plot(predictions, color="#1f77b4"):
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

    fig = plt.figure(figsize=(8, 3))
    plot(
        upset_data,
        fig=fig,
        element_size=15,
        sort_by="cardinality",
        facecolor=color,
        show_counts="%d",
        show_percentages="{:.0%}",
    )
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


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
            upset_plot(predictions)
        else:
            st.error("Please upload a file.")


render_form("prediction_form", "MLOmix-processed GEX or DNAm data")

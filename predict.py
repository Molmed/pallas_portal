import streamlit as st
import pandas as pd
from mlflow_client import MlflowClient
import matplotlib.pyplot as plt
from upsetplot import plot
import plotly.graph_objects as go
from collections import defaultdict
from pathlib import Path
import ast


st.set_page_config(
    page_title="PALLAS Predictions",
    layout="wide",
)

st.markdown(
    """
    <style>
    body {
        zoom: 0.8; /* 90% */
    }
    </style>
    """,
    unsafe_allow_html=True,
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
    plt.rcParams['font.size'] = 10
    plot(
        upset_data,
        fig=fig,
        element_size=30,
        sort_by="cardinality",
        facecolor=color,
        show_counts="%d",
        show_percentages=False
    )
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


def parse_prediction_classes(value):
    if isinstance(value, (list, tuple, set, frozenset)):
        return [normalize_label(item) for item in value]

    value = str(value).strip()

    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        parsed = value.split(";")

    if isinstance(parsed, (list, tuple, set, frozenset)):
        return [normalize_label(item) for item in parsed]

    return [normalize_label(parsed)]


def prediction_sets_summary(predictions, labels=None):
    prediction_sets = [
        set(parse_prediction_classes(value))
        for value in predictions["prediction"]
    ]

    summary = [
        {
            "Statistic": "Certain sets (size=1)",
            "Value": sum(len(values) == 1 for values in prediction_sets),
        },
        {
            "Statistic": "Uncertain sets (size >= 2)",
            "Value": sum(len(values) >= 2 for values in prediction_sets),
        },
        {
            "Statistic": "Empty sets (size=0)",
            "Value": sum(len(values) == 0 for values in prediction_sets),
        },
    ]

    if labels is not None:
        true_labels = labels.iloc[:, 0].map(normalize_label)
        labeled_rows = true_labels != "EMPTY SET"
        false_negatives = sum(
            true_label not in prediction_set
            for true_label, prediction_set, is_labeled in zip(
                true_labels,
                prediction_sets,
                labeled_rows,
            )
            if is_labeled
        )
        labeled_count = int(labeled_rows.sum())
        fnr = false_negatives / labeled_count if labeled_count else 0.0
        summary.append({
            "Statistic": "Overall False Negative Rate (FNR)",
            "Value": f"{fnr:.1%}",
        })

    return pd.DataFrame(summary)


def normalize_label(value):
    EMPTY_SET_LABEL = "EMPTY SET"
    if pd.isna(value):
        return EMPTY_SET_LABEL
    value = str(value).strip()
    if value == "" or value.lower() == "nan":
        return EMPTY_SET_LABEL
    return value


def sankey(df: pd.DataFrame,
           true_col: str = "true_label",
           pred_col: str = "prediction_sets",
           title: str = "Conformal prediction sets"
           ) -> go.Figure:

    palette_path = Path(__file__).resolve().parent / "conf" / "class_colors.tsv"
    palette_df = pd.read_csv(palette_path, sep="\t", header=None, names=["class", "color"], index_col=0)

    # Count flows: (true_label, predicted_label) → count
    flow_counts: dict[tuple[str, str], int] = defaultdict(int)

    for _, row in df.iterrows():
        true = normalize_label(row[true_col])
        preds = parse_prediction_classes(row[pred_col])

        for pred in preds:
            flow_counts[(true, pred)] += 1

    true_labels = sorted({k[0] for k in flow_counts})
    pred_labels = sorted({k[1] for k in flow_counts})

    # Right-side node labels get a suffix so identical names don't collapse
    suffix = " "
    pred_labels_display = [f"{p}{suffix}" for p in pred_labels]

    all_labels = true_labels + pred_labels_display
    label_index = {label: i for i, label in enumerate(all_labels)}

    sources, targets, values = [], [], []
    for (true, pred), count in flow_counts.items():
        sources.append(label_index[true])
        targets.append(label_index[f"{pred}{suffix}"])
        values.append(count)

    # generate palette from the palette_df
    palette = palette_df["color"].tolist()
    node_colors = [palette[i % len(palette)] for i in range(len(all_labels))]

    # Extend palette so all "(pred)" nodes have the same color as their corresponding true label node
    for i, label in enumerate(all_labels):
        if label.endswith(suffix):
            true_label = label[:-len(suffix)]  # remove suffix
            if true_label in true_labels:
                true_index = true_labels.index(true_label)
                node_colors[i] = node_colors[true_index]

    def hex_to_rgba(hex_color, alpha=0.8):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    link_colors = [hex_to_rgba(node_colors[s], 0.5) for s in sources]

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=15,
            thickness=15,
            line = dict(color = "black", width = 0.5),
            label=all_labels,
            color=node_colors,
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors  # color links based on source node
        ),
    ))

    fig.update_layout(
        title_text=title,
        title_font=dict(size=20),
        height=500 + 40 * max(len(true_labels), len(pred_labels)),
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(family="Arial, sans-serif", size=16, color="black")
    )
    st.plotly_chart(fig, use_container_width=True)


def render_form(form_id, uploader_label):
    form_column, output_column = st.columns([1, 2], gap="large")

    with form_column:
        st.subheader("Acute leukemia classification")
        with st.form(form_id, border=False):
            model = st.selectbox(
                "Select a model",
                mlflow_models,
                help="Select the model to use for prediction.",
            )
            tolerance_column, color_column = st.columns([5, 1])
            with tolerance_column:
                slider = st.slider("Error tolerance α", 0, 100, 5)
            with color_column:
                plot_color = st.color_picker("Plot color", "#9768ac")
            upload = st.file_uploader(uploader_label, type=["csv"])
            labels_upload = st.file_uploader(
                "If subtypes are known, upload labels (optional)",
                type=["csv"],
            )
            submitted = st.form_submit_button("Submit")

    if not submitted:
        return

    if upload is None:
        with form_column:
            st.error("Please upload a file.")
        return

    data = pd.read_csv(upload, index_col=0)

    labels = None
    if labels_upload is not None:
        try:
            labels = pd.read_csv(labels_upload, index_col=0)
        except Exception as e:
            with form_column:
                st.error(f"Error reading labels file: {e}")
            return

    predictions = mlflow_client.predict(
        model,
        data,
        slider,
        labels=labels,
    )

    with form_column:
        st.subheader("Summary")
        st.dataframe(
            prediction_sets_summary(predictions, labels),
            use_container_width=True,
            hide_index=True
        )

    with output_column:
        st.subheader("Conformal prediction sets")
        st.dataframe(
            predictions,
            use_container_width=True,
        )

        st.subheader("Conformal prediction set membership")
        upset_plot(predictions, color=plot_color)

        if labels is not None:
            sankey_data = pd.DataFrame({
                "true_label": labels.iloc[:, 0],
                "prediction_sets": predictions["prediction"],
            })
            st.subheader("True vs predicted subtype")
            sankey(sankey_data, title="")


render_form("prediction_form", "MLOmix-processed GEX or DNAm data")

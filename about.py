import streamlit as st

st.set_page_config(
    page_title="PALLAS10k Portal",
    layout="centered",
)

st.title("PALLAS10k Portal")

st.markdown(
    "This portal lets you classify acute leukemias using PALLAS10k, which was "
    "trained on over 10,000 Gene Expression and DNA methylation samples."
)

st.markdown(
    "## Usage"
)

st.markdown(
    "### Prepare your data"
)
st.markdown(
    "To prepare data for inference, please use the [MLOmix pipeline v1.0.0](https://github.com/Molmed/mlomix/tree/v1.0.0)."
)

st.markdown(
    "The `finalize` folder of the pipeline output should contain:"
)

st.markdown(
    "- `features.gex.csv`: Gene Expression data in CSV format, and/or\n"
    "- `features.dnam.csv`: DNA methylation data in CSV format, and\n"
    "- `labels.csv`: if you have specified known subtypes for your samples (optional)."
)

st.markdown(
    "### Classify"
)

st.markdown(
    "Once you have your data ready, click the **Predict** button below."
)

if st.button("Predict", icon="🔮"):
    st.switch_page("predict.py")

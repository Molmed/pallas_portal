import streamlit as st
import time


def show_progress():
    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'


def render_form(id, uploader_label):
    form = st.form(id, border=False)
    upload = form.file_uploader(uploader_label, type=["csv", "tsv", "txt"])
    slider = form.slider("Error tolerance", 0, 100, 90)

    # Every form must have a submit button.
    submitted = form.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider)
        show_progress()


gex_tab, dnam_tab = st.tabs(["Gene Expresssion", "DNA Methylation"])
with gex_tab:
    render_form("gex_form", "Upload Gene Expression Data")
with dnam_tab:
    render_form("dnam_form", "Upload DNA Methylation Data")

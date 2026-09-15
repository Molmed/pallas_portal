import base64
from pathlib import Path

import streamlit as st

# Define the pages
about = st.Page("about.py", title="About", icon="🧭")
predict = st.Page("predict.py", title="Predict", icon="🔮")
team = st.Page("team.py", title="Team", icon="🧑‍🔬")

# Set up navigation
pg = st.navigation([about, predict, team])

logo_path = Path(__file__).parent / "assets" / "mlomix_logo.png"
logo_data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
stylesheet_path = Path(__file__).parent / "styles.css"
st.markdown(
	f"<style>{stylesheet_path.read_text()}</style>",
	unsafe_allow_html=True,
)
st.sidebar.markdown(
	'<div class="mlomix-footer">'
	'<div class="mlomix-footer-label">Powered by</div>'
	'<a href="https://github.com/Molmed/mlomix">'
	f'<img src="data:image/png;base64,{logo_data}" alt="MLOmix">'
	'</a></div>',
	unsafe_allow_html=True,
)


# Run the selected page
pg.run()

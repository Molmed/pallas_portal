import streamlit as st

# Define the pages
about = st.Page("about.py", title="About", icon="🧭")
predict = st.Page("predict.py", title="Predict", icon="🔮")

# Set up navigation
pg = st.navigation([about, predict])

# Run the selected page
pg.run()

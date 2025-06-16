import streamlit as st

# Define the pages
about = st.Page("about.py", title="About", icon="🧭")
predict = st.Page("predict.py", title="Predict", icon="🔮")
team = st.Page("team.py", title="Team", icon="🧑‍🔬")

# Set up navigation
pg = st.navigation([about, predict, team])

# Run the selected page
pg.run()

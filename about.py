import streamlit as st

st.title("PALLAS Portal")

"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porta justo metus. Fusce aliquet pretium lacus ut vulputate. Sed ac nisl hendrerit, eleifend arcu vitae, efficitur velit. Vivamus commodo urna vitae elit porttitor, sit amet laoreet felis fringilla. Mauris tempus pellentesque libero, malesuada dictum metus pretium ac. Nam gravida enim id velit condimentum, at placerat tellus aliquam. Mauris cursus elementum velit ac ultrices. Mauris non massa nec justo eleifend vulputate."

"Vestibulum posuere quis justo vitae convallis. Nullam dui odio, suscipit ornare dapibus sed, tempus accumsan nunc. Aenean condimentum nibh ac tellus accumsan dapibus. Nullam quis arcu sed arcu placerat tristique. Cras egestas enim vitae turpis convallis suscipit. Aenean scelerisque tellus at tellus consequat lacinia. Cras quis accumsan nulla. Donec ante dolor, ornare in vestibulum sed, vehicula a diam. Vestibulum efficitur viverra tortor quis sollicitudin. Proin dictum turpis ornare, pharetra risus a, commodo justo."

col1, col2 = st.columns(2)
with col1:
    st.link_button("Gene expression data preprocessing 👉", "http://www.example.com/gene-expression")

with col2:
    st.link_button("DNA methylation data preprocessing 👉", "http://www.example.com/gene-expression")

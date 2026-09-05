import streamlit as st

st.title("PALLAS Contributors")

st.markdown(
    "The following individuals have contributed to the development of "
    "PALLAS10k, the classifier powering the PALLAS Portal."
)

st.markdown(
    """
    Mariya Lysenkova Wiklander<sup>1,2</sup>,
    Emma Dizdarevic<sup>1,2</sup>,
    Dave Zachariah<sup>3</sup>,
    Olga Krali<sup>1,2</sup>,
    Tatjana Pandzic<sup>4</sup>,
    Nina Hollfelder<sup>2,4</sup>,
    Ola Wallerman<sup>2,4</sup>,
    Gisela Barbany<sup>5</sup>,
    Lucia Cavelier Franco<sup>5</sup>,
    Jesper Eisfeldt<sup>5</sup>,
    Linda Holmfeldt<sup>4</sup>,
    Aleksandra Krstic Drago<sup>5</sup>,
    Pierre de Langen<sup>5</sup>,
    Kajsa Paulsson<sup>6</sup>,
    Fatemah Rezayee<sup>5</sup>,
    Minjun Yang<sup>6</sup>,
    Vasilios Zachariadis<sup>7,8</sup>,
    Ingegerd Öfverholm<sup>5</sup>,
    Panagiotis Baliakas<sup>2,4</sup>,
    Josefine Palle<sup>9</sup>,
    Arja Harila<sup>9</sup>,
    Jessica Nordlund<sup>1,2</sup>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    1. Department of Medical Sciences, Uppsala University, Uppsala, Sweden
    2. SciLifeLab, Uppsala University, Uppsala, Sweden
    3. Department of Information Technology, Uppsala University, Uppsala, Sweden
    4. Department of Immunology, Genetics, and Pathology, Uppsala University, Uppsala, Sweden
    5. Department of Molecular Medicine and Surgery, Karolinska Institutet, Stockholm, Sweden
    6. Division of Clinical Genetics, Department of Laboratory Medicine, Lund University, Lund, Sweden
    7. Department of Oncology-Pathology, Karolinska Institutet, Stockholm, Sweden
    8. Paediatric Oncology, Astrid Lindgren Children's Hospital, Karolinska University Hospital, Stockholm, Sweden
    9. Department of Woman's and Children's Health, Uppsala University, Uppsala, Sweden
    """
)

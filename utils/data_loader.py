import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Le fichier {path} est introuvable.")
        return pd.DataFrame()

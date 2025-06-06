import dill
import streamlit as st

@st.cache_resource
def load_model(path="code/final_model/rl_model.pkl"):
    with open(path, "rb") as f:
        return dill.load(f)

import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Prédiction du BANK CHURN",
        page_icon="🧠",
        layout="wide"
    )

    # Appliquer style CSS
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

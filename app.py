import streamlit as st
from config.setting import setup_page
from pages import accueil, analyse, prediction, apropos


st.title("🏡 **Application de Prédiction du BANK CHURN**")

# Configuration de la page
setup_page()


# Fonction pour changer la page active dans st.session_state
def set_page(page_name):
    st.session_state.page = page_name

# Barre de navigation horizontale avec des boutons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Accueil"):
        set_page("Accueil")
with col2:
    if st.button("📊 Analyse"):
        set_page("Analyse")
with col3:
    if st.button("🔍 Prédiction"):
        set_page("Prédiction")
with col4:
    if st.button("ℹ️ A-propos"):
        set_page("A-propos")
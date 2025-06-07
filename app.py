import streamlit as st
from config.setting import setup_page
from pages import accueil, analyse, prediction, apropos

# Configuration de la page
setup_page()

# Navigation
PAGES = {
    "🏠 Accueil": accueil,
    "📊 Analyse": analyse,
    "🔍 Prédiction": prediction,
    "ℹ️ A-propos": apropos
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller à :", list(PAGES.keys()))

# Affichage de la page choisie
PAGES[selection].app()

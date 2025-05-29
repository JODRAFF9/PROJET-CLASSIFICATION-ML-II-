import streamlit as st
import pandas as pd
import numpy as np


# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction du BANK CHURN ", layout="wide")

# Fonction pour charger les données (mise en cache)
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} est introuvable.")
        return pd.DataFrame()

# Chargement des données
train_df = load_data("data/cleaned data/train_df.csv")
train_df_labelled = load_data("data/cleaned data/train_df.csv")

# Initialisation de l'état de la page (si ce n'est pas déjà fait)
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# Titre de l'application
st.title("🏡 **Application de Prédiction du BANK CHURN**")

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


# Section Accueil
if st.session_state.page == "Accueil":
    st.write("---")
    st.header("Bienvenue 👋")
    st.write("""
        Cette application vous offre des outils intuitifs pour :
        - 🟡 Prédire le **BANK CHURN** à partir de caractéristiques clés.
        - 📊 Analyser les **du BANK CHURN**
    """)

    st.info("Utilisez la barre de navigation pour explorer les différentes fonctionnalités.")

# Section Analyse
elif st.session_state.page == "Analyse":
    st.subheader("📊 Analyse des Données")
    if st.checkbox("Afficher les données brutes"):
        st.dataframe(train_df_labelled)

    st.write("### Statistiques descriptives")
    st.write(train_df_labelled.describe())

    st.write("### Visualisation de deux variables")
    variable_x = st.selectbox("Variable X", train_df_labelled.columns)
    variable_y = st.selectbox("Variable Y", train_df_labelled.columns)

    # Visualisation des relations entre les variables
    fig, ax = plt.subplots(figsize=(10, 8))
    if train_df_labelled[variable_x].dtype in ['int64', 'float64'] and train_df_labelled[variable_y].dtype in ['int64', 'float64']:
        sns.scatterplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, color="teal", s=100, edgecolor='black')
        ax.set_title(f"Nuage de points entre {variable_x} et {variable_y}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel(variable_y, fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
    elif train_df_labelled[variable_x].dtype == 'object' and train_df_labelled[variable_y].dtype == 'object':
        grouped_train_df_labelled = train_df_labelled.groupby([variable_x, variable_y]).size().unstack()
        grouped_train_df_labelled.plot(kind='bar', stacked=True, ax=ax, cmap='coolwarm')
        ax.set_title(f"Graphique en barres empilées de {variable_x} par {variable_y}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel("Effectifs", fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
        ax.legend(title=variable_y, fontsize=12)
    else:
        sns.boxplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, palette="Set2")
        ax.set_title(f"Graphique de boîte de {variable_y} par {variable_x}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel(variable_y, fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)

    st.pyplot(fig)
    st.write("---")

    st.write("### Matrice de Corrélation")
    correlation_matrix = train_df_labelled.select_dtypes(include=['int64', 'float64']).corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    fig_corr, ax_corr = plt.subplots(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", mask=mask, fmt=".2f")
    st.pyplot(fig_corr)
    st.write("---")

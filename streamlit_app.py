import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
train_df_labelled=train_df.drop(['id',"CustomerId","Surname"], axis=1)

binary_mapping = {0: 'No', 1: 'Yes'}
binary_cols = ['HasCrCard', 'IsActiveMember', 'Exited']

cat_cols = ['Geography', 'Gender', 'Tenure', 'NumOfProducts', 'HasCrCard',
       'IsActiveMember']

num_cols = ['CreditScore', 'Age', 'Balance', 'EstimatedSalary']

target = 'Exited'

for col in binary_cols:
    train_df_labelled[col] = train_df_labelled[col].map(binary_mapping)


def nom_variable(nom_variable):
    """
    Renvoie un nom descriptif avec espaces pour une variable de dataset bancaire.

    Args:
        nom_variable (str): Nom original de la variable

    Returns:
        str: Nom descriptif avec espaces
    """
    correspondance = {
        'id': "l'dentifiant unique",
        'CustomerId': "l'identifiant du client",
        'Surname': 'le nom du client',
        'CreditScore': "le score de crédit",
        'Geography': 'le pays de résidence',
        'Gender': 'le genre du client',
        'Age': "l'âge du client",
        'Tenure': 'la durée de relation client',
        'Balance': 'le solde du compte',
        'NumOfProducts': 'le nombre de produits souscrits',
        'HasCrCard': "la possession d'une carte crédit",
        'IsActiveMember': "le statut de membre actif",
        'EstimatedSalary': "le revenu annuel estimé",
        'Exited': "l'indicateur d'attrition"
    }

    # Retourne le nom descriptif ou le nom original si non trouvé
    return correspondance.get(nom_variable, nom_variable)

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
with col4:
    if st.button("🔍 A-propos"):
        set_page("A-propos")


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
        st.dataframe(train_df.head(100))
    
    st.write("### Statistiques descriptives")
    st.write(train_df_labelled[num_cols].describe())

    st.write("### Visualisation de deux variables")
    variable_x = st.selectbox("Variable X", train_df_labelled.columns)
    variable_y = st.selectbox("Variable Y", train_df_labelled.columns)
    
    nomx=nom_variable(variable_x)
    nomy=nom_variable(variable_y)
    
    # Visualisation des relations entre les variables
    fig, ax = plt.subplots(figsize=(10, 8))
    if train_df_labelled[variable_x].dtype in ['int64', 'float64'] and train_df_labelled[variable_y].dtype in ['int64', 'float64']:
        sns.scatterplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, color="teal", s=100, edgecolor='black')
        ax.set_title(f"Nuage de points entre {nomx} et {nomy}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel(variable_y, fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
    elif train_df_labelled[variable_x].dtype == 'object' and train_df_labelled[variable_y].dtype == 'object':
        grouped_train_df_labelled = train_df_labelled.groupby([variable_x, variable_y]).size().unstack()
        grouped_train_df_labelled.plot(kind='bar', stacked=True, ax=ax, cmap='coolwarm')
        ax.set_title(f"Graphique en barres empilées de {nomx} par {nomy}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel("Effectifs", fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)
        ax.legend(title=variable_y, fontsize=12)
    else:
        sns.boxplot(data=train_df_labelled, x=variable_x, y=variable_y, ax=ax, palette="Set2")
        ax.set_title(f"Graphique de boîte de {nomy} par {nomx}", fontsize=16, fontweight='bold')
        ax.set_xlabel(variable_x, fontsize=14)
        ax.set_ylabel(variable_y, fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12,rotation=45)

    st.pyplot(fig)
    st.write("---")

    st.write("### Matrice de Corrélation")
    correlation_matrix = train_df_labelled[num_cols].corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    fig_corr, ax_corr = plt.subplots(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", mask=mask, fmt=".2f")
    st.pyplot(fig_corr)
    st.write("---")

# Section Accueil
if st.session_state.page == "Prédiction":
    st.write("---")
    
# Section Accueil
if st.session_state.page == "A-propos":
    st.write("---")
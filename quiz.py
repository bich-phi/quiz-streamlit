import streamlit as st
import pandas as pd
import random

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
df = pd.read_excel("questions.xlsx")

# Normalisation des textes
for col in ["categorie", "sous_categorie", "sous_sous_categorie"]:
    df[col] = df[col].astype(str).str.strip().str.lower()

# -----------------------------
# INITIALISATION SESSION STATE
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df.copy()


# -----------------------------
# FONCTIONS
# -----------------------------
def appliquer_filtre(cat=None, souscat=None, soussouscat=None):
    """Filtre les questions selon le niveau choisi."""

    # Niveau 3 : sous-sous-catégorie (global)
    if soussouscat:
        st.session_state.filtered_df = df[df["sous_sous_categorie"] == soussouscat]

    # Niveau 2 : sous-catégorie (global)
    elif souscat:
        st.session_state.filtered_df = df[df["sous_categorie"] == souscat]

    # Niveau 1 : catégorie (local)
    elif cat:
        st.session_state.filtered_df = df[df["categorie"] == cat]

    # Aucun filtre → tout
    else:
        st.session_state.filtered_df = df.copy()

    st.session_state.filtered_df = st.session_state.filtered_df.reset_index(drop=True)
    nouvelle_question()


def nouvelle_question():
    """Tire une nouvelle question au hasard."""
    if st.session_state.filtered_df.empty:
        st.session_state.current_question = "Aucune question dans cette catégorie."
        st.session_state.current_answer = ""
        return

    ligne = st.session_state.filtered_df.sample(1).iloc[0]
    st.session_state.current_question = ligne["question"]
    st.session_state.current_answer = ligne["reponse"]


def bonne_reponse():
    st.session_state.score += 1
    st.session_state.total += 1
    nouvelle_question()


def mauvaise_reponse():
    st.session_state.total += 1
    nouvelle_question()


# -----------------------------
# INTERFACE STREAMLIT
# -----------------------------
st.title("Quiz d'entraînement")

# Score
st.markdown(f"### Score : {st.session_state.score}/{st.session_state.total}")

# -----------------------------
# MENU HIÉRARCHIQUE
# -----------------------------

# --- Niveau 1 : Catégorie ---
categories = sorted(df["categorie"].unique())
cat = st.selectbox("Choisir une catégorie (ou laisser vide) :", [""] + categories)

# --- Niveau 2 : Sous-catégorie dépendante ---
if cat:
    sous_categories = sorted(df[df["categorie"] == cat]["sous_categorie"].unique())
else:
    sous_categories = sorted(df["sous_categorie"].unique())

souscat = st.selectbox("Choisir une sous-catégorie (optionnel) :", [""] + sous_categories)

# --- Niveau 3 : Sous-sous-catégorie dépendante ---
if souscat:
    sous_sous_categories = sorted(df[df["sous_categorie"] == souscat]["sous_sous_categorie"].unique())
else:
    sous_sous_categories = sorted(df["sous_sous_categorie"].unique())

soussouscat = st.selectbox("Choisir une sous-sous-catégorie (optionnel) :", [""] + sous_sous_categories)

# Bouton appliquer
if st.button("Jouer"):
    appliquer_filtre(
        cat if cat != "" else None,
        souscat if souscat != "" else None,
        soussouscat if soussouscat != "" else None
    )

# -----------------------------
# AFFICHAGE QUESTION
# -----------------------------
if st.session_state.current_question:
    st.markdown(f"## {st.session_state.current_question}")
else:
    st.markdown("## Cliquez sur *Jouer* pour commencer.")

# Bouton afficher réponse
if st.button("Afficher la réponse"):
    st.markdown(f"**Réponse :** {st.session_state.current_answer}")

# Boutons bonne/mauvaise réponse
col1, col2 = st.columns(2)

with col1:
    if st.button("Bonne réponse"):
        bonne_reponse()

with col2:
    if st.button("Mauvaise réponse"):
        mauvaise_reponse()

import streamlit as st
import pandas as pd
import random

# Charger les questions
df = pd.read_excel("questions.xlsx")

# Transformer la colonne categories en listes
df["categories"] = df["categories"].apply(
    lambda x: [c.strip().lower() for c in str(x).split(",")]
)

# Extraire toutes les catégories uniques
all_categories = set()
for cats in df["categories"]:
    all_categories.update(cats)

all_categories = sorted(list(all_categories))
all_categories.insert(0, "toutes")

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
def appliquer_filtre(choix):
    """Filtre les questions selon la catégorie choisie."""
    if choix == "toutes":
        st.session_state.filtered_df = df.copy()
    else:
        st.session_state.filtered_df = df[
            df["categories"].apply(lambda cats: choix in cats)
        ]

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

# Menu catégories
choix = st.selectbox("Choisir une catégorie :", all_categories)

if st.button("Appliquer le filtre"):
    appliquer_filtre(choix)

# Affichage question
if st.session_state.current_question:
    st.markdown(f"## {st.session_state.current_question}")
else:
    st.markdown("## Cliquez sur *Appliquer le filtre* pour commencer.")

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


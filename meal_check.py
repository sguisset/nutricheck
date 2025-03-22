import streamlit as st
import requests
import base64

st.set_page_config(page_title="Analyse Repas Santé", layout="centered")
st.title("Analyse intelligente de ton repas")

st.markdown("Cette application détecte les aliments à partir d'une photo et analyse leur impact selon ton régime personnalisé (sarcoïdose, protéinurie, acide urique, régime LUV).")

# --- 1. Upload de l’image et reconnaissance automatique ---
st.header("1. Téléverse une photo de ton repas")

uploaded_file = st.file_uploader("Choisis une image", type=["jpg", "jpeg", "png"])

detected_food = []

if uploaded_file is not None:
    st.image(uploaded_file, caption="Ton repas", use_column_width=True)

    image_bytes = uploaded_file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    st.write("Analyse automatique en cours...")

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/analyze"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "448e007b0fmsh689d7d5d6621861p10e37fjsn72e1ee5e6e1c",  # <<< Remplace par ta clé personnelle
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.post(url, json={"image": encoded_image},
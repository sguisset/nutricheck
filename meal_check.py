import streamlit as st
import requests

st.set_page_config(page_title="Analyse Repas Santé", layout="centered")
st.title("Analyse intelligente de ton repas")

st.markdown("Cette application détecte les aliments à partir d'une photo et analyse leur impact selon ton régime personnalisé (sarcoïdose, protéinurie, acide urique, régime LUV).")

# --- 1. Upload de l’image et reconnaissance automatique ---
st.header("1. Téléverse une photo de ton repas")

uploaded_file = st.file_uploader("Choisis une image", type=["jpg", "jpeg", "png"])
detected_food = []

if uploaded_file is not None:
    st.image(uploaded_file, caption="Ton repas", use_container_width=True)

    st.write("Analyse automatique en cours...")

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/analyze"

    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }

    headers = {
        "X-RapidAPI-Key": "TA_CLE_API_ICI",  # 🔁 Remplace ici avec ta clé RapidAPI
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "category" in data:
            aliment_detecte = data["category"]["name"]
            st.success(f"Aliment détecté : **{aliment_detecte}**")
            detected_food.append(aliment_detecte.capitalize())
        else:
            st.warning("Aucun aliment détecté.")
    else:
        st.error(f"Erreur {response.status_code} lors de l’analyse.")

# --- 2. Sélection manuelle (modifiable) ---
st.header("2. Vérifie ou complète les aliments présents")

liste_aliments = [
    "Tofu", "Œuf", "Saumon", "Poulet", "Pois chiches", "Lentilles", "Riz basmati", "Quinoa",
    "Pain de seigle", "Pain complet", "Avocat", "Amandes", "Graines de courge", "Brocolis", "Courgettes",
    "Épinards", "Fenouil", "Carottes", "Betteraves", "Tomates", "Concombres", "Cerises", "Myrtilles",
    "Poire", "Pomme", "Dattes", "Fromage blanc", "Yaourt nature", "Gyoza végétarien", "Aubergines"
]

selection = st.multiselect("Quels aliments sont présents ?", options=liste_aliments, default=detected_food)

# --- 3. Analyse santé simplifiée ---
st.header("3. Résultat de l'analyse")

def analyse(selection):
    score = 0
    remarques = []

    if any(a in {"Tofu", "Pois chiches", "Lentilles"} for a in selection):
        score += 1
        remarques.append("✔ Bon apport en protéines végétales.")

    if any(a in {"Œuf", "Saumon", "Poulet"} for a in selection):
        score += 0.5
        remarques.append("ℹ️ Protéines animales présentes (à modérer en cas de protéinurie).")

    if any(a in {"Lentilles", "Pois chiches", "Saumon", "Dattes"} for a in selection):
        score -= 0.5
        remarques.append("⚠️ Aliments modérément riches en purines présents.")

    if any(a in {"Avocat", "Amandes", "Graines de courge"} for a in selection):
        score += 1
        remarques.append("✔ Bons lipides anti-inflammatoires présents.")

    if any(a in {"Épinards", "Fenouil", "Concombres", "Betteraves", "Courgettes"} for a in selection):
        score += 1
        remarques.append("✔ Aliments alcalins bons pour les reins.")

    if any(a in {"Cerises", "Myrtilles", "Poire", "Pomme"} for a in selection):
        score += 1
        remarques.append("✔ Fruits riches en antioxydants présents.")

    if score >= 3.5:
        conclusion = "✅ Repas équilibré et adapté à ton profil."
    elif 2 <= score < 3.5:
        conclusion = "🟡 Repas correct, quelques ajustements possibles."
    else:
        conclusion = "🔴 Repas à modérer selon tes objectifs santé."

    return conclusion, remarques

if selection:
    conclusion, remarques = analyse(selection)
    st.subheader("🧾 Conclusion :")
    st.success(conclusion)

    st.subheader("🔍 Détails :")
    for r in remarques:
        st.markdown(f"- {r}")
else:
    st.info("👉 Sélectionne ou détecte des aliments pour afficher l’analyse.")

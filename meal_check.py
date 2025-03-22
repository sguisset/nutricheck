import streamlit as st

st.set_page_config(page_title="Meal Analysis", layout="centered")
st.title("Analyse de ton repas")
st.markdown("Cette application évalue ton repas selon ton répas")

st.header("1. Téléverse une photo (optionnel)")
st.file_uploader("Image du repas (non utilisée pour l’instant)", type=["jpg", "jpeg", "png"])

st.header("2. Sélectionne les aliments présents dans ton repas")
aliments = [
    "Tofu", "Œuf", "Saumon", "Poulet", "Pois chiches", "Lentilles", "Riz basmati", "Quinoa",
    "Pain de seigle", "Pain complet", "Avocat", "Amandes", "Graines de courge", "Brocolis", "Courgettes",
    "Épinards", "Fenouil", "Carottes", "Betteraves", "Tomates", "Concombres", "Cerises", "Myrtilles",
    "Poire", "Pomme", "Dattes", "Fromage blanc", "Yaourt nature", "Gyoza végétarien", "Aubergines"
]
selection = st.multiselect("Quels aliments sont présents ?", aliments)

st.header("3. Résultat de l'analyse")

def analyse(selection):
    score = 0
    remarques = []

    proteines_veg = {"Tofu", "Pois chiches", "Lentilles"}
    if any(a in proteines_veg for a in selection):
        score += 1
        remarques.append("✔ Bon apport en protéines végétales.")

    proteines_anim = {"Œuf", "Saumon", "Poulet"}
    if any(a in proteines_anim for a in selection):
        score += 0.5
        remarques.append("ℹ️ Protéines animales présentes (à modérer si protéinurie).")

    purines = {"Lentilles", "Pois chiches", "Saumon", "Dattes"}
    if any(a in purines for a in selection):
        score -= 0.5
        remarques.append("⚠️ Présence d’aliments modérément riches en purines.")

    bons_lipides = {"Avocat", "Amandes", "Graines de courge"}
    if any(a in bons_lipides for a in selection):
        score += 1
        remarques.append("✔ Présence de bons lipides anti-inflammatoires.")

    alcalins = {"Épinards", "Fenouil", "Concombres", "Betteraves", "Courgettes"}
    if any(a in alcalins for a in selection):
        score += 1
        remarques.append("✔ Aliments alcalinisants présents, bon pour les reins.")

    antioxydants = {"Cerises", "Myrtilles", "Poire", "Pomme"}
    if any(a in antioxydants for a in selection):
        score += 1
        remarques.append("✔ Fruits riches en antioxydants présents.")

    if score >= 3.5:
        conclusion = "✅ Repas équilibré et bien adapté à ton régime."
    elif 2 <= score < 3.5:
        conclusion = "🟡 Repas correct, mais quelques ajustements possibles."
    else:
        conclusion = "🔴 Ce repas est à modérer selon tes objectifs santé."

    return conclusion, remarques

if selection:
    conclusion, remarques = analyse(selection)
    st.subheader("🧾 Conclusion :")
    st.success(conclusion)

    st.subheader("🔎 Détails :")
    for r in remarques:
        st.markdown(f"- {r}")
else:
    st.info("👉 Sélectionne les aliments pour afficher l’analyse.")

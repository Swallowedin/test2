import streamlit as st
from openai import OpenAI
import json
import os

st.set_page_config(page_title="View Avocats - Estimation IA", page_icon="⚖️", layout="wide")

# Importation des tarifs
from tarifs_prestations import get_tarifs
tarifs = get_tarifs()

# Configuration du client OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Vous êtes un assistant juridique."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message.content.strip()

def analyze_question(question: str, client_type: str, urgency: str):
    prompt = f"""Analysez la question suivante et déterminez le domaine juridique et la prestation la plus pertinente.

Question : {question}
Type de client : {client_type}
Degré d'urgence : {urgency}

Répondez au format JSON strict suivant :
{{
    "domaine": "nom du domaine juridique",
    "prestation": "nom de la prestation",
    "indice_confiance": 0.0 à 1.0
}}
"""
    response = get_openai_response(prompt)
    result = json.loads(response)
    return result['domaine'], result['prestation'], result['indice_confiance']

def calculate_estimate(domaine: str, prestation: str, urgency: str):
    tarif = tarifs['prestations'].get(domaine, {}).get(prestation, {}).get('tarif', 0)
    if urgency == "Urgent":
        tarif = round(tarif * 1.5)
    return tarif

def main():
    st.title("🏛️ View Avocats - EstimiIA")

    client_type = st.selectbox("Vous êtes :", ("Particulier", "Entreprise"))
    urgency = st.selectbox("Degré d'urgence :", ("Normal", "Urgent"))
    question = st.text_area("Expliquez brièvement votre cas :", height=150)

    if st.button("Obtenir une estimation"):
        if question:
            domaine, prestation, confidence = analyze_question(question, client_type, urgency)
            tarif = calculate_estimate(domaine, prestation, urgency)

            st.success("Analyse terminée. Voici les résultats :")
            st.write(f"**Domaine juridique :** {domaine}")
            st.write(f"**Prestation :** {prestation}")
            st.write(f"**Estimation :** {tarif} €HT")
            st.write(f"**Indice de confiance :** {confidence:.2%}")

            if confidence < 0.5:
                st.warning("⚠️ Attention : L'estimation peut manquer de précision.")

    st.markdown("---")
    st.write("© 2024 View Avocats. Tous droits réservés.")

if __name__ == "__main__":
    main()

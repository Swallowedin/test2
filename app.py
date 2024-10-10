import streamlit as st
from openai import OpenAI
import json
import os
from tarifs_prestations import calculer_tarif, get_tarifs

st.set_page_config(page_title="View Avocats - Estimation IA", page_icon="⚖️", layout="wide")

# Configuration du client OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY n'est pas défini dans les variables d'environnement")

client = OpenAI(api_key=OPENAI_API_KEY)

# Obtention des tarifs
tarifs = get_tarifs()

def get_openai_response(prompt: str, model: str = "gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Vous êtes un assistant juridique spécialisé."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message.content.strip()

def analyze_question(question: str, client_type: str, urgency: str):
    options = [f"{domaine}: {', '.join(prestations_domaine.keys())}" for domaine, prestations_domaine in tarifs['prestations'].items()]
    prompt = f"""Analysez la question suivante et déterminez le domaine juridique et la prestation la plus pertinente.

Question : {question}
Type de client : {client_type}
Degré d'urgence : {urgency}

Options de domaines et prestations :
{' '.join(options)}

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
    is_urgent = urgency == "Urgent"
    return calculer_tarif(domaine, prestation, urgence=is_urgent)

def main():
    st.title("🏛️ View Avocats - EstimiIA")

    client_type = st.selectbox("Vous êtes :", ("Particulier", "Entreprise"))
    urgency = st.selectbox("Degré d'urgence :", ("Normal", "Urgent"))
    question = st.text_area("Expliquez brièvement votre cas juridique :", height=150)

    if st.button("Obtenir une estimation"):
        if question:
            with st.spinner("Analyse en cours..."):
                domaine, prestation, confidence = analyze_question(question, client_type, urgency)
                tarif = calculate_estimate(domaine, prestation, urgency)

            st.success("Analyse terminée. Voici les résultats :")
            
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Détails de l'estimation")
                st.write(f"**Domaine juridique :** {tarifs['prestations'].get(domaine, {}).get('label', domaine)}")
                st.write(f"**Prestation :** {tarifs['prestations'].get(domaine, {}).get(prestation, {}).get('label', prestation)}")
                st.write(f"**Indice de confiance :** {confidence:.2%}")

            with col2:
                st.subheader("Estimation tarifaire")
                st.markdown(f"<h1 style='text-align: center; color: #1f77b4;'>À partir de<br>{tarif} €HT</h1>", unsafe_allow_html=True)

            if confidence < 0.5:
                st.warning("⚠️ Attention : L'estimation peut manquer de précision en raison d'un faible indice de confiance.")

            st.info("Cette estimation est fournie à titre indicatif. Pour une évaluation précise, nous vous recommandons de contacter directement notre cabinet.")

    st.markdown("---")
    st.write("© 2024 View Avocats. Tous droits réservés.")

if __name__ == "__main__":
    main()

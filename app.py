import streamlit as st
import requests
import json
from tarifs_prestations import get_tarifs

# Configuration de l'API OpenAI
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = st.secrets["OPENAI_API_KEY"]

def analyze_request(user_input):
    """Analyse la demande de l'utilisateur avec ChatGPT en utilisant des requêtes HTTP directes."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Vous êtes un assistant juridique. Identifiez la prestation juridique demandée par l'utilisateur."},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Erreur lors de l'appel à l'API OpenAI: {response.status_code}")
        return None

def find_matching_service(analyzed_request, tarifs):
    """Trouve la prestation correspondante dans la base de données des tarifs."""
    for category in tarifs['prestations'].values():
        for service, details in category.items():
            if service == 'label':
                continue
            if analyzed_request.lower() in details['label'].lower():
                return details
    return None

def main():
    st.title("Estimateur de tarif pour prestations juridiques")

    user_input = st.text_area("Décrivez la prestation juridique dont vous avez besoin :")

    if st.button("Estimer le tarif"):
        if user_input:
            with st.spinner("Analyse en cours..."):
                analyzed_request = analyze_request(user_input)
                if analyzed_request:
                    tarifs = get_tarifs()
                    matching_service = find_matching_service(analyzed_request, tarifs)

                    if matching_service:
                        st.success(f"Prestation identifiée : {matching_service['label']}")
                        st.info(f"Tarif estimé : {matching_service['tarif']} €")
                        st.write(f"Description : {matching_service['definition']}")
                    else:
                        st.warning("Aucune prestation correspondante n'a été trouvée. Veuillez reformuler votre demande.")
        else:
            st.error("Veuillez entrer une description de la prestation souhaitée.")

if __name__ == "__main__":
    main()

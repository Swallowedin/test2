import streamlit as st
from openai import OpenAI
from tarifs_prestations import get_tarifs

# Configuration du client OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_request(user_input):
    """Analyse la demande de l'utilisateur avec ChatGPT."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant juridique. Identifiez la prestation juridique demandée par l'utilisateur."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API OpenAI: {str(e)}")
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

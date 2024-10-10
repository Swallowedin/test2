def get_tarifs():
    return {
        "prestations": {
            "droit_civil_contrats": {
                "label": "Droit civil et contrats",
                "redaction_conditions_generales": {
                    "label": "Rédaction des conditions générales",
                    "tarif": 800,
                },
                "redaction_contrat_mise_disposition_prestations_services_associes": {
                    "label": "Rédaction de contrat de mise à disposition avec prestations de services associées",
                    "tarif": 1500,
                },
                "consultation_initiale": {
                    "label": "Consultation initiale",
                    "tarif": 200,
                },
                "consultation_juridique_et_reglementaire": {
                    "label": "Consultation juridique et réglementaire",
                    "tarif": 800,
                },
                "creation_entreprise": {
                    "label": "Création d'entreprise",
                    "tarif": 3000,
                },
            },
            "droit_immobilier_commercial": {
                "label": "Droit immobilier et commercial",
                "redaction_bail_commercial": {
                    "label": "Rédaction de bail commercial",
                    "tarif": 1500,
                },
                "redaction_bail_commercial_en_etat_futur_achevement_BEFA": {
                    "label": "Rédaction de bail commercial en état futur d'achèvement (BEFA)",
                    "tarif": 2500,
                },
                "redaction_bail_commercial_derogatoire": {
                    "label": "Rédaction de bail commercial dérogatoire",
                    "tarif": 1000,
                },
            },
            "droit_procedures_collectives": {
                "label": "Droit des procédures collectives",
                "redaction_declaration_creance": {
                    "label": "Rédaction de déclaration de créance",
                    "tarif": 500,
                },
                "contestation_creance_juge_commissaire": {
                    "label": "Contestation de créance devant le juge-commissaire",
                    "tarif": 1000,
                },
                "declaration_cessation_paiements": {
                    "label": "Déclaration de cessation des paiements",
                    "tarif": 800,
                },
            },
            "contentieux_des_affaires": {
                "label": "Contentieux des affaires",
                "redaction_mise_en_demeure": {
                    "label": "Rédaction de mise en demeure",
                    "tarif": 300,
                },
                "requete_injonction_payer": {
                    "label": "Requête en injonction de payer",
                    "tarif": 600,
                },
                "negociation_redaction_protocole_accord_transactionnel": {
                    "label": "Négociation et rédaction de protocole d'accord transactionnel",
                    "tarif": 1000,
                },
            },
        },
        "facteur_urgence": 1.5
    }

def calculer_tarif(domaine, prestation, urgence=False):
    tarifs = get_tarifs()
    tarif_base = tarifs["prestations"].get(domaine, {}).get(prestation, {}).get("tarif", 0)
    
    if urgence:
        return tarif_base * tarifs["facteur_urgence"]
    return tarif_base

if __name__ == "__main__":
    # Test de la fonction
    print(calculer_tarif("droit_civil_contrats", "redaction_conditions_generales"))
    print(calculer_tarif("droit_civil_contrats", "redaction_conditions_generales", urgence=True))

import requests
import streamlit as st


# Fonction pour faire une prédiction via l'API
def get_prediction(region: str, cereal: str, superficie: int, pluie: int) -> dict:
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"region": region,
                  "cereal": cereal,
                  "superficie": superficie,
                  "pluie": pluie}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la connexion à l'API: {str(e)}")
        return None


# Fonction pour obtenir les informations du modèle
def get_model_info():
    try:
        response = requests.get("http://localhost:8000/model-info")
        return response.json()
    except requests.exceptions.RequestException:
        return None

import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Production d'Arachides",
    page_icon="🥜",
    layout="wide"
)

# Fonction pour faire une prédiction via l'API
def get_prediction(superficie: float, pluie: float) -> dict:
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"superficie": superficie, "pluie": pluie}
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

# Initialisation de l'historique des prédictions
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []


# Styles CSS
st.markdown(
    """
    <style>
    .column-left {
        background-color: #FFDDC1; /* Couleur pêche */
        padding: 10px;
        border-radius: 10px;
    }
    .column-center {
        background-color: #DFFFD6; /* Couleur vert pâle */
        padding: 10px;
        border-radius: 10px;
    }
    .column-right {
        background-color: #C1DFFF; /* Couleur bleu clair */
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Interface utilisateur
st.markdown("<h1 class='main-header'>🥜 Prédiction de la Production d'Arachides</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 class='sub-header'>ℹ️ Informations sur le modèle</h2>", unsafe_allow_html=True)
    model_info = get_model_info()
    if model_info:
        st.write("Type de modèle:", model_info["model_type"])
        st.write("Variables utilisées:")
        for feature in model_info["features"]:
            st.write(f"- {feature}")
        st.markdown("### Coefficients du modèle")
        coef_df = pd.DataFrame({
            'Variable': ['Superficie', 'Pluie', 'Constante'],
            'Coefficient': [
                model_info['coefficients']['superficie'],
                model_info['coefficients']['pluie'],
                model_info['coefficients']['intercept']
            ]
        })
        st.dataframe(coef_df)
    else:
        st.warning("Impossible de charger les informations du modèle")

col1, col2 ,col3= st.columns([1,3,1])

with col1:
    st.markdown("<h3 class='sub-header'>📊 Entrée des données</h3>", unsafe_allow_html=True)
    superficie = st.number_input(
        "Superficie (hectares)",
        min_value=1000.0,
        max_value=1000000.0,
        value=485703.0,
        step=1000.0,
        format="%f"
    )
    pluie = st.number_input(
        "Pluviométrie (mm)",
        min_value=0.0,
        max_value=2000.0,
        value=723.0,
        step=10.0,
        format="%f"
    )

with col2:
    st.markdown("<h3 class='sub-header'>🎯 Résultats de la prédiction</h3>", unsafe_allow_html=True)
    if st.button("Faire une prédiction", type="primary"):
        with st.spinner("Calcul de la prédiction en cours..."):
            prediction = get_prediction(superficie, pluie)
            if prediction:
                st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
                st.metric(
                    label="Production prédite",
                    value=f"{prediction['prediction']:,.0f} tonnes"
                )
                st.write(f"Prédiction faite le: {prediction['timestamp']}")
                st.markdown("</div>", unsafe_allow_html=True)

                # Ajout de la prédiction à l'historique
                new_prediction = {
                    'timestamp': prediction['timestamp'],
                    'superficie': superficie,
                    'pluie': pluie,
                    'prediction': prediction['prediction']
                }
                st.session_state.prediction_history.append(new_prediction)

# Affichage de l'historique des prédictions
st.markdown("<h3 class='sub-header'>📝 Historique des prédictions</h3>", unsafe_allow_html=True)
if st.session_state.prediction_history:
    history_df = pd.DataFrame(st.session_state.prediction_history)
    st.dataframe(
        history_df,
        column_config={
            'timestamp': 'Date et heure',
            'superficie': 'Superficie (ha)',
            'pluie': 'Pluie (mm)',
            'prediction': st.column_config.NumberColumn(
                'Production prédite (tonnes)',
                format="%.0f"
            )
        },
        hide_index=True
    )
else:
    st.info("Aucune prédiction n'a encore été effectuée")

# Bouton pour télécharger l'historique
if st.session_state.prediction_history:
    csv = pd.DataFrame(st.session_state.prediction_history).to_csv(index=False)
    st.download_button(
        label="📥 Télécharger l'historique",
        data=csv,
        file_name=f'historique_predictions_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

with col3 :
    st.markdown('<div class="column-right">Contenu de la colonne droite</div>', unsafe_allow_html=True)
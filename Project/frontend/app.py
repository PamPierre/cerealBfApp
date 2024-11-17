# app.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Production d'Arachides au BF",
    page_icon="🥜",
    layout="wide"
)

# Fonction pour faire une prédiction via l'API
def get_prediction(superficie: float, pluie: float) -> dict:
    """Appelle l'API pour obtenir une prédiction"""
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
    """Récupère les informations sur le modèle depuis l'API"""
    try:
        response = requests.get("http://localhost:8000/model-info")
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Style CSS personnalisé
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1F618D;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2874A6;
            margin-bottom: 1rem;
        }
        .prediction-box {
            background-color: #F7F9F9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# En-tête de l'application
st.markdown("<h1 class='main-header'>🥜 Prédiction de la Production d'Arachides au BF</h1>", unsafe_allow_html=True)

# Sidebar pour les informations sur le modèle
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

# Corps principal de l'application
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 class='sub-header'>📊 Entrée des données</h3>", unsafe_allow_html=True)
    
    # Widgets pour les entrées utilisateur
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
                
                # Création du graphique
                fig = go.Figure()
                
                # Ajout des indicateurs
                fig.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=prediction['prediction'],
                    title={'text': "Production prédite (tonnes)"},
                    gauge={
                        'axis': {'range': [None, 1000000]},
                        'steps': [
                            {'range': [0, 300000], 'color': "lightgray"},
                            {'range': [300000, 600000], 'color': "gray"},
                            {'range': [600000, 1000000], 'color': "darkgray"}
                        ],
                        'bar': {'color': "#1F618D"}
                    }
                ))
                
                fig.update_layout(
                    height=400,
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)

# Section historique des prédictions
st.markdown("<h3 class='sub-header'>📝 Historique des prédictions</h3>", unsafe_allow_html=True)

# Création d'une clé dans la session state pour stocker l'historique s'il n'existe pas déjà
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# Ajout de la nouvelle prédiction à l'historique si elle existe
if 'prediction' in locals() and prediction:
    new_prediction = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'superficie': superficie,
        'pluie': pluie,
        'prediction': prediction['prediction']
    }
    st.session_state.predictions_history.append(new_prediction)

# Affichage de l'historique dans un tableau
if st.session_state.predictions_history:
    history_df = pd.DataFrame(st.session_state.predictions_history)
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
if st.session_state.predictions_history:
    csv = pd.DataFrame(st.session_state.predictions_history).to_csv(index=False)
    st.download_button(
        label="📥 Télécharger l'historique",
        data=csv,
        file_name=f'historique_predictions_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Développé avec ❤️ par AFRICADATAENTRY(ADE) la prédiction de la production d'arachides au Burkina Faso</p>
    </div>
""", unsafe_allow_html=True)

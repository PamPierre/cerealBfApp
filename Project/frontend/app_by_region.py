from collections import Counter

import streamlit as st
from appelApi import get_prediction,get_model_info
from datetime import datetime
import pandas as pd
from barreLateralGauche import plotLatteralGauche
from presentationDelaDonneFiltre import presentationData
from st_circular_progress import CircularProgress
import time

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Production d'Arachides",
    page_icon="🥜",
    layout="wide"
)



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
dataObservation = pd.read_csv("../../data/observation_indicateurs_regions_cereal.csv")
dataObservationMerge = pd.read_csv("../../data/all_cereal_merge.csv")

listKeyVal = ['Date', 'Superficie', 'Production', 'Pluie par année']
dataObservation["Date"] = dataObservation["Date"].apply(int)
dataObservation["Value"] = dataObservation["Value"].apply(lambda v: int(str(v).replace(" ", "").replace("u202f", "")))

for l in listKeyVal:
    dataObservationMerge[l] = dataObservationMerge[l].apply(
        lambda v: int(str(v).replace(" ", "").replace("u202f", "")))
dataObservation = dataObservationMerge.copy()

cols = ["indicateur", "région", "céréales", "Date"]

kpi = {k: sorted(dataObservation[k].unique()) for k in cols if k in dataObservation.keys()}

# Interface utilisateur
with st.sidebar:
    regCheck = plotLatteralGauche(st,kpi) # Permet de recuperer les valeurs des checkbox

presentationData(regCheck = regCheck,dataObservation=dataObservation,st=st)


col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 class='sub-header'>📊 Entrée des données</h3>", unsafe_allow_html=True)
    with st.expander(f"Choix de la région"):
        region_radio = st.radio("Région",kpi["région"])
    with st.expander(f"Choix du céréal a prédire"):
        cereal_radio = st.radio("céréales",kpi["céréales"])
    superficie = st.number_input(
        "Superficie (ha)",
        min_value=1.0,
        max_value=1000000.0,
        value=485703.0,
        step=10.0,
        format="%f"
    )
    pluie = st.number_input(
        "Pluviométrie (Nombre de pluie par année)",
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
            prediction = get_prediction(region=region_radio,cereal=cereal_radio,superficie=superficie, pluie=pluie)
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
                    'Région' : region_radio,
                    'Céreal' : cereal_radio,
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

from collections import Counter
import altair as alt

def presentationData(regCheck,dataObservation,st):
    cereal = regCheck["céréales"]

    statCheckboxCereal = Counter(cereal.values())
    cerealAffiche = f"{statCheckboxCereal[True]} céréals"
    if True in statCheckboxCereal.keys():
        if statCheckboxCereal[True] <= 2:
            cerealAffiche = [k for k, v in cereal.items() if v == True]
            if len(cerealAffiche) == 1:
                cerealAffiche = cerealAffiche[0]
            else:
                cerealAffiche = ' et '.join(cerealAffiche).lower().replace("arachide", "l'arachide")
    st.markdown(f"<h1 class='main-header'>🥜 Prédiction de la Production de {cerealAffiche}</h1>",
                unsafe_allow_html=True)

    indicateur = [k for k, v in regCheck["indicateur"].items() if v == True]
    regions = [k for k, v in regCheck["région"].items() if v == True]
    cereales = [k for k, v in regCheck["céréales"].items() if v == True]
    dates = [k for k, v in regCheck["Date"].items() if v == True]
    try:
        st.markdown(f"<h2 class='main-header'>Présentation de la data par {indicateur[0]}</h2>", unsafe_allow_html=True)
    except:
        st.markdown(
            f"<h2 class='main-header'>Présentation de la data(Faites vos filtre dans la barre latteral Gauche</h2>",
            unsafe_allow_html=True)

    dataObservationForFront = dataObservation[(dataObservation["indicateur"].isin(indicateur)) &
                                              (dataObservation["région"].isin(regions)) &
                                              (dataObservation["céréales"].isin(cereales)) &
                                              (dataObservation["Date"].isin(dates))]

    dataObservationForFront = dataObservationForFront.sort_values(by=["Date"], ascending=False)

    try:
        max_val = max(dataObservationForFront['Value'].values.tolist())
        min_val = min(dataObservationForFront['Value'].values.tolist())
        exactVal = st.slider(label='Valeur Indicateur',
                             min_value=min_val,
                             max_value=max_val, value=max_val)  # 👈 this is a widget
    except:
        max_val = max(dataObservation['Value'].values.tolist())
        min_val = min(dataObservation['Value'].values.tolist())
        exactVal = st.slider(label='Valeur Indicateur',
                             min_value=min_val,
                             max_value=max_val, value=max_val)  # 👈 this is a widget
    dataObservationForFront = dataObservationForFront[dataObservationForFront["Value"] <= exactVal]
    default = ["région", "céréales", "Date", "Value"]
    showData, chartData = st.columns(2)
    with showData:
        st.dataframe(dataObservationForFront[default].head(30), hide_index=True)

    with chartData:
        chart = alt.Chart(dataObservationForFront).mark_bar().encode(
            x=alt.X("Date", title="Date"),  # Agréger par Date
            y=alt.Y("Value:Q", title="Quantité totale"),  # Somme des valeurs par date
            color=alt.Color("céréales:N", title="céréale"),  # Couleurs selon les céréales
            size=alt.Size("Value:Q", title="Taille des valeurs"),
            tooltip=["région:N", "céréales:N", "Date", "Value:Q"]  # Infos au survol
        ).properties(
            width=800,
            height=400,
            title="Histogramme par Date et Type de Céréales"
        )

        # Afficher le graphique dans Streamlit
        st.altair_chart(chart, use_container_width=True)
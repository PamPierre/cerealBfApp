from collections import Counter
import altair as alt
import pandas as pd
from sliders import createSlider
import folium
from streamlit_folium import st_folium

region_lon_lat = pd.read_csv("../../data/region_long_lat.csv")
cereales_couleurs = {
    "Arachide": "orange",
    "Coton": "white",
    "Maïs": "yellow",
    "Mil": "brown",
    "Niebé": "green",
    "Riz": "beige",
    "Sorgho": "red"
}

def presentationData(regCheck, dataObservation, st):
    global region_lon_lat
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

    # indicateur = [k for k, v in regCheck["indicateur"].items() if v == True]
    regions = [k for k, v in regCheck["région"].items() if v == True]
    cereales = [k for k, v in regCheck["céréales"].items() if v == True]
    dates = [k for k, v in regCheck["Date"].items() if v == True]
    try:
        pass
        # st.markdown(f"<h2 class='main-header'>Présentation de la data par {indicateur[0]}</h2>", unsafe_allow_html=True)
    except:
        st.markdown(
            f"<h2 class='main-header'>Présentation de la data(Faites vos filtre dans la barre latteral Gauche</h2>",
            unsafe_allow_html=True)

    # (dataObservation["indicateur"].isin(indicateur)) &
    dataObservationForFront = dataObservation[(dataObservation["région"].isin(regions)) &
                                              (dataObservation["céréales"].isin(cereales)) &
                                              (dataObservation["Date"].isin(dates))]

    dataObservationForFront = dataObservationForFront.sort_values(by=["Date"], ascending=False)

    superficie_val, rain_val, production_val = createSlider(st, dataObservationForFront, dataObservation)
    dataObservationForFront = dataObservationForFront[(dataObservationForFront["Superficie"] <= superficie_val) &
                                                      (dataObservationForFront["Pluie par année"] <= rain_val) &
                                                      (dataObservationForFront["Production"] <= production_val)]

    default = ["région", "céréales", "Date", 'Superficie', 'Pluie par année', "Production"]
    showData, chartData, mapData = st.columns(3)
    with showData:
        st.title("Donnée")
        st.dataframe(dataObservationForFront[default].head(30), hide_index=True)
        # Regrouper les données par 'Value' et calculer des statistiques (par exemple, la somme)
        grouped_data = (
            dataObservationForFront.groupby("Production")
            .agg({"région": "count", "céréales": "nunique", "Date": "min"})
            .rename(columns={
                "région": "Nombre de régions",
                "céréales": "Nombre de types de céréales",
                "Date": "Première date"
            })
            .reset_index()
        )

        # Afficher les données groupées dans Streamlit
        # st.write("### Données regroupées par `Value`")
        # st.dataframe(grouped_data.head(30), hide_index=True)

    with chartData:
        chart = alt.Chart(dataObservationForFront).mark_circle().encode(
            x=alt.X("Superficie:Q", title="Superficie (ha)"),  # Superficie sur l'axe X
            y=alt.Y("Production:Q", title="Production (tonnes)"),  # Production sur l'axe Y
            size=alt.Size("Production:Q", title="Pluie (mm)", scale=alt.Scale(range=[10, 100])),
            # Taille des bulles par Pluie
            color=alt.Color("céréales:N", title="Type de Céréale"),  # Couleur selon le type de céréale
            tooltip=["région:N", "céréales:N", "Superficie:Q", "Production:Q", "Pluie par année:Q"]  # Infos au survol
        ).properties(
            width=800,
            height=400,
            title="Bubble Chart : Superficie, Production et Pluie par Type de Céréale"
        )

        # Afficher le graphique dans Streamlit
        st.title("Production par superficie")
        st.altair_chart(chart, use_container_width=True)

    with mapData:

        # Créer une carte centrée sur le Burkina Faso
        m = folium.Map(location=[12.2383, -1.5616], zoom_start=6)
        offset = 0.3  # Déplacement en degrés (~1 km)
        for c in Counter(dataObservationForFront["céréales"]).keys():
            index = 0
            data_for_map = region_lon_lat.copy()
            data_for_map["Production"] = data_for_map["région"].apply(
                lambda v: sum(
                    dataObservationForFront[(dataObservationForFront["région"] == v) & (dataObservationForFront["céréales"] == c)]["Production"].values.tolist()))
            data = data_for_map[data_for_map["Production"]>0]

            # Ajouter les villes à la carte avec des cercles proportionnels à la superficie
            for _, row in data.iterrows():
                lat_offset = (index % 3 - 1) * offset  # Décalage en latitude (-offset, 0, +offset)
                lon_offset = (index // 3 - 1) * offset  # Décalage en longitude (-offset, 0, +offset)
                folium.Circle(
                    location=[row['latitude'] + lat_offset, row['longitude'] + lon_offset],
                    radius=row['Production']/100,  # Ajuster le rayon pour la visibilité
                    color=cereales_couleurs[c],
                    fill=True,
                    fill_color='bleu',
                    popup=f"Région : {row['région']}\nCéréal : {c}\nProduction : {row['Production']} Tonnes"
                ).add_to(m)
            index += 1

        # Afficher la carte dans Streamlit
        st.title("Production par région Au Burkina Faso")
        st_folium(m, width=800, height=500)

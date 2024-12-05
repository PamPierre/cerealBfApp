

def createSlider(st,dataObservationForFront,dataObservation):
    production_slider, superficie_slider, rain_slider = st.columns(3)
    with superficie_slider:
        try:
            max_val = max(dataObservationForFront['Superficie'].values.tolist())
            min_val = min(dataObservationForFront['Superficie'].values.tolist())
            superficie_val = st.slider(label='Superficie',
                                       min_value=min_val,
                                       max_value=max_val, value=max_val)  # 👈 this is a widget
        except:
            max_val = max(dataObservation['Superficie'].values.tolist())
            min_val = min(dataObservation['Superficie'].values.tolist())
            superficie_val = st.slider(label='Valeur Indicateur',
                                       min_value=min_val,
                                       max_value=max_val,
                                       value=max_val)  # 👈 this is a widget
    with rain_slider:
        try:
            max_val = max(dataObservationForFront['Pluie par année'].values.tolist())
            min_val = min(dataObservationForFront['Pluie par année'].values.tolist())
            rain_val = st.slider(label='Pluie par année',
                                       min_value=min_val,
                                       max_value=max_val, value=max_val)  # 👈 this is a widget
        except:
            max_val = max(dataObservation['Pluie par année'].values.tolist())
            min_val = min(dataObservation['Pluie par année'].values.tolist())
            rain_val = st.slider(label='Pluie par année',
                                       min_value=min_val,
                                       max_value=max_val, value=max_val)  # 👈 this is a widget

    with production_slider:
        try:
            max_val = max(dataObservationForFront['Production'].values.tolist())
            min_val = min(dataObservationForFront['Production'].values.tolist())
            production_val = st.slider(label='Production',
                                 min_value=min_val,
                                 max_value=max_val, value=max_val)  # 👈 this is a widget
        except:
            max_val = max(dataObservation['Production'].values.tolist())
            min_val = min(dataObservation['Production'].values.tolist())
            production_val = st.slider(label='Production',
                                 min_value=min_val,
                                 max_value=max_val, value=max_val)  # 👈 this is a widget
    return superficie_val,rain_val,production_val
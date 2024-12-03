import pandas as pd
from appelApi import get_model_info

def plotLatteralGauche(st,kpi):
    regCheck = {}
    st.markdown("<h2 class='sub-header'>ℹ️ Informations sur le modèle</h2>", unsafe_allow_html=True)
    model_info = get_model_info()
    if model_info:
        # st.write("Type de modèle:", model_info["model_type"])
        st.write("Variables")
        for k, v in kpi.items():
            with st.expander(f"📋 Liste des {k} (cliquez pour dérouler)"):
                regCheck[k] = {i: st.checkbox(f"{i}", value=True if i in ["Evolution de la production par région selon le type de céréales","Burkina Faso","Arachide"]+kpi["Date"][-5:] else False) for i in v}
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
    return regCheck
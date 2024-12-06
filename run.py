import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
 
st.write("""
# My first app
Hello *Ade*
""")

df = pd.read_csv("data/donnée_arrachide.csv")

df = df.rename(columns={"Arachide produit":"Production","Arachide Supperficie":"Superficie","Pluie par année":"Pluie"})
for k in df.keys():
  df[k] = df[k].apply(lambda v : int(str(v).replace(" ","").replace("u202f","")))

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)


st.line_chart(df,x="Année",y=["Production", "Superficie"])

hist_data = df[["Année","Pluie"]]

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data,group_labels = hist_data["Année"])

# Plot!
st.plotly_chart(fig, use_container_width=True)

""" my_circular_progress = CircularProgress(
                        label="Sample Bar",
                        value=0,
                        key="my_circular_progress")
my_circular_progress.st_circular_progress()
for i in range(100):
    my_circular_progress.update_value(progress=i)
    #time.sleep(0.3)
"""
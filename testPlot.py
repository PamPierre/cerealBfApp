import pandas as pd
from collections import Counter
#dataObservation = pd.read_csv("../data/observation_indicateurs_regions_cereal.csv")
dataObservation = pd.read_csv("data/observation_indicateurs_regions_cereal.csv")
dataObservation["Date"] = dataObservation["Date"].apply(int)
cols = ["région","céréales","Date"]

kpi= {k : sorted(dataObservation[k].unique()) for k in cols}

print(kpi)

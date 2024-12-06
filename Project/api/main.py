# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import pickle
import numpy as np
from datetime import datetime

app = FastAPI(
    title="API de Prédiction de Production d'Arachides",
    description="API pour prédire la production d'arachides au Burkina Faso basée sur la superficie et la pluviométrie",
    version="1.0.1"
)


# Modèle Pydantic pour la validation des données d'entrée
class PredictionInput(BaseModel):
    superficie: int = Field(..., gt=0, description="Superficie en hectares")
    pluie: int = Field(..., gt=0, le=2000, description="Pluviométrie annuelle en mm")
    region : str
    cereal : str

    class Config:
        schema_extra = {
            "example": {
                "superficie": 485703,
                "pluie": 723
            }
        }


# Modèle Pydantic pour la réponse
class PredictionOutput(BaseModel):
    region : str
    cereal : str
    prediction: float
    superficie: float
    pluie: float
    timestamp: str
    unit: str = "tonnes"



# Chargement du modèle
try:
    # with open("modelArachideBf_v1.h5", 'rb') as file: old
    with open("model_production_all_cereales_RandomForest.h5", 'rb') as file:
        rf_model = pickle.load(file)
except Exception as e:
    raise Exception(f"Erreur lors du chargement du modèle: {str(e)}")

cereal_cat = {'Coton': 1,
  'Niebé': 2,
  'Riz': 3,
  'Maïs': 4,
  'Sorgho': 5,
  'Mil': 6,
  'Arachide': 7}

regionCat = {'Burkina Faso': 0,
  'Boucle du Mouhoun': 1,
  'Cascades': 2,
  'Centre': 3,
  'Centre-Est': 4,
  'Centre-Nord': 5,
  'Centre-Ouest': 6,
  'Centre-Sud': 7,
  'Est': 8,
  'Hauts-Bassins': 9,
  'Nord': 10,
  'Plateau Central': 11,
  'Sahel': 12,
  'Sud-Ouest': 13}

def prediction_global(region = "Burkina Faso", cereal = "Coton",superficie = 373407, plui = 102):
  global rf_model,regionCat,cereal_cat
  r = regionCat[region] # Conversion en variable categoriel
  c = cereal_cat[cereal] # Conversion en variable categoriel
  s = superficie
  p = plui
  return round(rf_model.predict([[r,c,s,p]])[0])


@app.get("/")
async def root():
    """
    Route racine de l'API
    """
    return {
        "message": "API de prédiction de production céréaliere dans toutes les regions du burkina",
        "version": "1.0.1",
        "endpoints": {
            "/predict": "Faire une prédiction",
            "/model-info": "Informations sur le modèle",
            "/health": "Statut de l'API"
        }
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Prédit la production d'arachides basée sur la superficie et la pluviométrie
    """
    try:
        # Préparation des données pour la prédiction
        # features = [[input_data.superficie, input_data.pluie]]

        # Faire la prédiction
        prediction = prediction_global(region= input_data.region,
                                       cereal=input_data.cereal,
                                       superficie=input_data.superficie,
                                       plui = input_data.pluie)

        # Création de la réponse
        response = PredictionOutput(
            prediction=float(prediction),
            superficie=input_data.superficie,
            pluie=input_data.pluie,
            region= input_data.region,
            cereal= input_data.cereal,
            timestamp=datetime.now().isoformat()
        )

        print(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-info")
async def model_info():
    """
    Retourne les informations sur le modèle
    """
    return {
        "model_type": "Random Regression",
        "features": ["région","céréale","superficie", "pluie"],
        "target": "production",
        "coefficients": {
            "superficie": 325000,
            "pluie": 102,
            "R²": 0.955
        },
        "unit": "tonnes"
    }


@app.get("/health")
async def health_check():
    """
    Vérifie l'état de santé de l'API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }



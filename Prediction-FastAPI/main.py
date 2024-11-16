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
    version="1.0.0"
)


# Modèle Pydantic pour la validation des données d'entrée
class PredictionInput(BaseModel):
    superficie: float = Field(..., gt=0, description="Superficie en hectares")
    pluie: float = Field(..., gt=0, le=2000, description="Pluviométrie annuelle en mm")

    class Config:
        schema_extra = {
            "example": {
                "superficie": 485703,
                "pluie": 723
            }
        }


# Modèle Pydantic pour la réponse
class PredictionOutput(BaseModel):
    prediction: float
    superficie: float
    pluie: float
    timestamp: str
    unit: str = "tonnes"


# Chargement du modèle
try:
    with open("modelArachideBf_v1.h5", 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    raise Exception(f"Erreur lors du chargement du modèle: {str(e)}")


@app.get("/")
async def root():
    """
    Route racine de l'API
    """
    return {
        "message": "API de prédiction de production d'arachides",
        "version": "1.0.0",
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
        features = [[input_data.superficie, input_data.pluie]]

        # Faire la prédiction
        prediction = model.predict(features)[0]

        # Création de la réponse
        response = PredictionOutput(
            prediction=float(prediction),
            superficie=input_data.superficie,
            pluie=input_data.pluie,
            timestamp=datetime.now().isoformat()
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model-info")
async def model_info():
    """
    Retourne les informations sur le modèle
    """
    return {
        "model_type": "Linear Regression",
        "features": ["superficie", "pluie"],
        "target": "production",
        "coefficients": {
            "superficie": float(model.coef_[0]),
            "pluie": float(model.coef_[1]),
            "intercept": float(model.intercept_)
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



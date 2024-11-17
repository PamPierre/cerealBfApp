# API de Prédiction de la Production d'Arachides

Cette API permet de prédire la production d'arachides au Sénégal en fonction de la superficie cultivée et de la pluviométrie.

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd prediction-arachides-api
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Démarrage de l'API

```bash
uvicorn main:app --reload
```

L'API sera accessible à l'adresse : http://localhost:8000

## Documentation de l'API

La documentation interactive de l'API est disponible à :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Endpoints

### 1. Prédiction (`POST /predict`)

Fait une prédiction de la production d'arachides basée sur la superficie et la pluviométrie.

Exemple de requête :
```json
{
    "superficie": 550333.4,
    "pluviometrie": 740.2
}
```

### 2. Information sur le modèle (`GET /model/info`)

Retourne les informations sur le modèle utilisé.

### 3. État de santé (`GET /health`)

Vérifie l'état de santé de l'API.

## Structure du Projet

```
prediction-arachides-api/
├── main.py           # Code principal de l'API
├── requirements.txt  # Dépendances Python
└── README.md        # Documentation
```

## Modèle

Le modèle utilisé est une régression linéaire multiple avec :
- R² : 0.80
- Variables : superficie cultivée et pluviométrie
- Unités :
  - Superficie : hectares
  - Pluviométrie : millimètres
  - Production : tonnes

## Test de l'API

Vous pouvez tester l'API avec curl :

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"superficie": 550333.4, "pluviometrie": 740.2}'
```

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

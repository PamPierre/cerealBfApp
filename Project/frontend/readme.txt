pip install -r requirements.txt

streamlit run app.py

project/
├── api/
│   ├── main.py (FastAPI)
│   ├── requirements.txt
│   └── modelArachideBf_v1.h5
└── frontend/
    ├── app.py (Streamlit)
    └── requirements.txt


cd api
uvicorn main:app --reload


cd frontend
streamlit run app.py
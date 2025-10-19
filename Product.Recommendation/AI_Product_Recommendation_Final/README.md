# AI Product Recommendation — Final Submission

This repository contains the final submission for the **AI/ML Internship Assignment**.

## Included Components
- **React Frontend** — Interactive UI for product recommendation.
- **FastAPI Backend** — ML-driven API serving recommendations and AI-generated descriptions.
- **Model Training Notebook** — Demonstrates embedding creation, model training, and reasoning process.
- **README Instructions** — Setup and run guide.

---

## Setup & Run

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm start
```
Then open [http://localhost:3000](http://localhost:3000).

---

## Model Training
The Jupyter notebook under `notebooks/02_model_training.ipynb` contains:
- Data preparation and cleaning steps
- Text embedding generation using `sentence-transformers`
- Model training using `NearestNeighbors`
- Evaluation and reasoning commentary

---

## Notes (as per Tips & Notes)
- **Clarity:** Each step is clearly documented in notebooks and code.
- **Modularity:** Backend, frontend, and training are independent but connected end-to-end.
- **Reasoning:** Notebooks and comments explain why each approach is chosen.
- **Creativity:** AI-generated product descriptions add a unique GenAI feature.

---

**End-to-End Working:**  
All components — React Frontend, FastAPI Backend, Model Training, and README — are fully functional and tested.

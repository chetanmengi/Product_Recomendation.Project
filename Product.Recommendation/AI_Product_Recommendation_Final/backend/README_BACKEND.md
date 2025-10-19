# Backend (FastAPI)

## Run
1. Create virtualenv and install:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints
- `POST /api/query` — body: `{ "query": "<text>", "k": 5 }` returns nearest product matches.
- `POST /api/generate` — body: `{ "query": "<text>", "k": 5 }` returns matches with generated descriptions.

## Notes
- Embeddings are computed with `sentence-transformers` and cached at `app/models/embeddings.joblib`.
- If you change the dataset, delete the embeddings cache to regenerate.

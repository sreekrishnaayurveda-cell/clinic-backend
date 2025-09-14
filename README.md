# Sreekrishna Ayurveda Backend

A minimal FastAPI backend to store and fetch patient data for your Sreekrishna Ayurveda Custom GPT via Actions.

## Quick Start (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./test.db
export API_KEY=devkey123
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Deploy (Render/Railway/Heroku)

1. Create a PostgreSQL database and copy the full connection string.
2. Set environment variables on your hosting service:
   - `DATABASE_URL` = your Postgres connection string
   - `API_KEY` = a long random value (used by the GPT Action)
3. Start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. After deploy, visit `/docs` to test.

## Endpoints
- `POST /patients` → Create patient
- `GET /patients/{id}` → Get patient
- `POST /observations` → Create observation
- `GET /observations/{id}` → Get observation
- `GET /health` → Health check

## Auth
All endpoints require header `X-API-Key: <your API_KEY>`.

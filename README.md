# agente-pastorino

Chat con base de datos (PostgreSQL) usando FastAPI + OpenAI.

## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Probar
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"decime cuantas facturas están impagas"}'
```
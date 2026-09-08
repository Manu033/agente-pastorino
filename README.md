# agente-pastorino

Agente de consultas internas sobre PostgreSQL usando FastAPI + OpenAI. El agente
solo puede leer las tablas declaradas en `ALLOWED_TABLES`, genera una única
consulta de lectura y responde usando exclusivamente sus resultados.

## Configuración

Usá un usuario de PostgreSQL de solo lectura (`DB_USER`) y completá
`SCHEMA_DESCRIPTION` con las tablas y columnas reales. No agregues credenciales ni
datos sensibles al esquema enviado al modelo.

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
  -d '{"question":"¿Cuántas facturas están impagas?"}'
```

La respuesta incluye `answer`, la consulta SQL validada y las filas obtenidas.
Las preguntas que no puedan resolverse con el esquema autorizado se rechazan.
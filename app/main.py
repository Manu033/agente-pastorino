from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import question_to_sql
from app.sql_guard import validate_sql
from app.db import run_query

app = FastAPI(title="agente-pastorino")

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    try:
        sql = question_to_sql(req.question)
        safe_sql = validate_sql(sql)
        rows = run_query(safe_sql)
        return {"question": req.question, "sql": safe_sql, "rows": rows, "count_rows": len(rows)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
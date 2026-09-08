import os
import re
from dotenv import load_dotenv

load_dotenv()

ALLOWED_TABLES = {t.strip().lower() for t in os.getenv("ALLOWED_TABLES", "").split(",") if t.strip()}
MAX_ROWS = int(os.getenv("MAX_ROWS", "100"))

FORBIDDEN = ["insert ", "update ", "delete ", "drop ", "alter ", "truncate ", "create ", "grant ", "revoke ", "comment ", "copy "]

def enforce_limit(sql: str) -> str:
    s = sql.strip().rstrip(";")
    if re.search(r"\blimit\s+\d+\b", s, flags=re.IGNORECASE):
        return s + ";"
    return f"{s} LIMIT {MAX_ROWS};"

def extract_tables(sql: str):
    matches = re.findall(r"\b(?:from|join)\s+([a-zA-Z0-9_\.]+)", sql, flags=re.IGNORECASE)
    return {m.split(".")[-1].lower() for m in matches}

def validate_sql(sql: str):
    s = sql.strip().lower()
    if not s.startswith("select"):
        raise ValueError("Solo se permiten consultas SELECT.")
    for word in FORBIDDEN:
        if word in s:
            raise ValueError(f"Consulta bloqueada por seguridad ({word.strip()}).")
    tables = extract_tables(sql)
    if ALLOWED_TABLES:
        not_allowed = tables - ALLOWED_TABLES
        if not_allowed:
            raise ValueError(f"Tablas no permitidas: {', '.join(not_allowed)}")
    return enforce_limit(sql)
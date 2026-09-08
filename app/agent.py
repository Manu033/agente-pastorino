import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Sos un asistente que convierte preguntas en SQL para PostgreSQL.
Reglas:
- Devolver SOLO SQL.
- Solo SELECT.
- Evitar columnas sensibles.
"""

def question_to_sql(question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()
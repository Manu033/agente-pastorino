import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCHEMA_DESCRIPTION = os.getenv(
    "SCHEMA_DESCRIPTION",
    """
Tablas disponibles:
- facturas(id, cliente_id, fecha_emision, fecha_vencimiento, importe, estado)
- clientes(id, nombre, cuit)
- pagos(id, factura_id, fecha_pago, importe)
Los estados de factura habituales son 'pagada' e 'impaga'.
""",
).strip()

SYSTEM_PROMPT = """
Sos un asistente interno de una empresa. Convertís preguntas sobre el negocio en
una única consulta SQL de solo lectura para PostgreSQL.
Reglas estrictas:
- Respondé SOLO SQL, sin Markdown ni explicaciones.
- Usá únicamente las tablas y columnas del esquema proporcionado.
- Usá SELECT (también se permite WITH que termine en SELECT); nunca modifiques datos.
- Si la pregunta no se puede responder con ese esquema o no trata sobre la empresa,
  devolvé exactamente OUT_OF_SCOPE.
- Para conteos o sumas devolvé una fila con un alias claro.
- No selecciones credenciales, secretos ni datos personales innecesarios.
"""


def question_to_sql(question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": f"{SYSTEM_PROMPT}\n\nESQUEMA AUTORIZADO:\n{SCHEMA_DESCRIPTION}",
            },
            {"role": "user", "content": question},
        ],
    )
    return (
        resp.choices[0].message.content.strip()
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )


def answer_from_rows(question: str, rows: list[dict]) -> str:
    """Resume únicamente el resultado obtenido, sin permitir que el modelo consulte."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Sos un asistente administrativo. Respondé en español, de forma "
                    "breve y clara. Usá exclusivamente los datos JSON entregados; "
                    "no inventes datos ni afirmes haber consultado otra fuente. "
                    "Si no hay filas, indicá que no se encontraron resultados."
                ),
            },
            {
                "role": "user",
                "content": f"Pregunta: {question}\nResultado JSON: {rows}",
            },
        ],
    )
    return resp.choices[0].message.content.strip()
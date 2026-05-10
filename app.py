print("🔥 FASTAPI STARTED")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from database import initialize_database, execute_query

app = FastAPI()

initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/generate-sql")
def generate_sql(request: QueryRequest):

    prompt = f"""
You are a senior SQL engineer.

Convert natural language to SQL.

CRITICAL RULES:
- Return ONLY SQL
- No explanations
- No markdown
- No backticks
- NEVER invent tables or columns

DATABASE SCHEMA:
Table: users
Columns:
- id
- name
- created_at (YYYY-MM-DD)

STRICT RULES:
- ONLY use table "users"
- ONLY use columns listed above
- NEVER use table_name or signup_date
- For year filtering use:
  strftime('%Y', created_at)

Question:
{request.question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    sql_query = result["response"].strip().replace("```sql", "").replace("```", "")

    try:
        query_results = execute_query(sql_query)
    except Exception as e:
        query_results = {"error": str(e)}

    return {
        "sql": sql_query,
        "results": query_results,
        "confidence": "high",
        "model": "llama3 (local)",
        "dialect": "sqlite"
    }
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

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

Convert natural language into PostgreSQL SQL.

Rules:
- Use PostgreSQL syntax only
- Return ONLY SQL
- No explanations

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

    return {
    "sql": result["response"].strip().replace("```sql", "").replace("```", ""),
    "confidence": "high",
    "model": "llama3 (local)",
    "dialect": "postgresql"
}
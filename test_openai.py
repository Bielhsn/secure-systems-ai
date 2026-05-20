import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Inicializa o cliente. Se sua variável no .env se chamar GEMINI_API_KEY,
# você pode usar apenas client = genai.Client() que ele puxa automaticamente.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
Analise esta arquitetura:

Frontend React
API Gateway
Microserviço de autenticação
Banco PostgreSQL

Retorne SOMENTE JSON válido:
{
  "components": [],
  "risks": [],
  "recommendations": [],
  "architecture_score": 0
}
"""

# Faz a chamada para a API passando configurações de sistema, temperatura e formato
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="Você é um arquiteto de software.",
        temperature=0.2,
        response_mime_type="application/json" # Força a saída para ser estritamente JSON
    )
)

content = response.text

print("Resposta bruta:")
print(content)

try:
    parsed = json.loads(content)
    print("\nJSON OK:")
    print(parsed)
except Exception as e:
    print("\nErro no JSON:")
    print(e)
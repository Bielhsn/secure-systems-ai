import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_architecture(text: str):
    prompt = f"""
Você é um arquiteto de software especialista em sistemas distribuídos.

Analise o diagrama abaixo.

Texto extraído:
{text}

Retorne SOMENTE JSON válido neste formato:

{{
  "components": [],
  "risks": [],
  "recommendations": [],
  "architecture_score": 0
}}

Não escreva markdown.
Não use ```json.
Retorne apenas JSON puro.
"""

    response = model.generate_content(prompt)

    content = response.text.strip()

    # Guardrail básico
    content = content.replace("```json", "")
    content = content.replace("```", "").strip()

    try:
        return json.loads(content)

    except Exception:
        return {
            "error": "invalid_json_from_llm",
            "raw_response": content
        }
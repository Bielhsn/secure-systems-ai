import os
import json

from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_diagram_image(
    filepath: str
):

    image = Image.open(filepath)

    prompt = """
Você é um arquiteto de software
especialista em:

- microsserviços
- cloud computing
- APIs
- segurança
- sistemas distribuídos
- escalabilidade
- observabilidade

Analise o diagrama de arquitetura enviado.

Identifique:

1. Componentes arquiteturais
2. Possíveis riscos
3. Recomendações arquiteturais
4. Score da arquitetura

Retorne SOMENTE JSON válido:

{
  "components": [],
  "risks": [],
  "recommendations": [],
  "architecture_score": 0
}

Regras:
- score de 0 a 10
- máximo 5 riscos
- máximo 5 recomendações
- não usar markdown
- apenas JSON puro
"""

    response = model.generate_content(
        [prompt, image]
    )

    content = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(content)

    except Exception:
        return {
            "error":
            "invalid_json_from_llm",
            "raw_response":
            content
        }
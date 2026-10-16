import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

response = client.responses.create(
    model=os.getenv("OPENAI_MODEL"),
    input="""Extraia informações do evento: Daniel e Alberto vão gravar uma aula na terça-feira.
    EXEMPLO DA FORMATAÇÃO: {
        "formato_saida": {
            "pessoas": ["..."],
            "acao": "...",
            "tipo_evento": "...",
            "data": "..."
        }
    }
    """
)

print(response.output_text)
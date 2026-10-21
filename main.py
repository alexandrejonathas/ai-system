import json
import os

import requests
import yfinance as yf
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_URL"))


def search_kb(query: str):
    response = requests.post(
        "http://localhost:8000/ai/search", json={"query": query, "limit": 3}
    )
    return response.json()

tools = [
    {
        "type": "function",
        "name": "search_kb",
        "description": "Busca informações na base de conhecimento para responder perguntas.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A pergunta do usuario"
                }
            },
            "required": ["query"]
        }        
    }
]

input_list = [{"role": "user", "content": "Quais são os principais riscos financeiros da apple?"}]

response = client.responses.create(
    model=os.getenv("GROQ_MODEL"),
    tools=tools,
    input=input_list,
)

input_list.extend(response.output)

for item in response.output:

    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = search_kb(**args)
        
        text = [r["text"] for r in result["results"]]
        
        input_list.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({"results": text}, ensure_ascii=False)
            }
        )
        

final_response = client.responses.create(
    model=os.getenv("GROQ_MODEL"),
    instructions="Responda com uma análise baseada nos dados retornados pela função.",
    input=input_list,
    tools=tools
)

print(final_response.output_text)
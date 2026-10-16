import json
import os

import yfinance as yf
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_URL"))


def get_stock(ticker: str):
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    output = {
        "ticker": ticker,
        "company_name": info.get("shortName", ticker),
        "current_price": info.get("currentPrice", 0)
    }
    
    return json.dumps(output)

tools = [
    {
        "type": "function",
        "name": "get_stock",
        "description": "Retorna informações básicas de uma ação.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Símbolo da ação (ex: AAPL, NVDA)"
                }
            },
            "required": ["ticker"]
        }
    }
]

input_list = [{"role": "user", "content": "Qual o preço da ação da Apple?"}]

response = client.responses.create(
    model=os.getenv("GROQ_MODEL"),
    tools=tools,
    input=input_list,
)

input_list.extend(response.output)

for item in response.output:

    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = get_stock(**args)
        input_list.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result
            }
        )
        

final_response = client.responses.create(
    model=os.getenv("GROQ_MODEL"),
    instructions="Responda com uma análise baseada nos dados retornados pela função.",
    input=input_list,
    tools=tools
)

print(final_response.output_text)
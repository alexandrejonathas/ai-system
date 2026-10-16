import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model=os.getenv("OPENAI_MODEL"),
    input="""Daniel e Alberto vão gravar uma aula na terça-feira.""",
    instructions="Extraia informações do evento",
    text_format=CalendarEvent
)

print(response.output_text)

event = response.output_parsed

print(event.model_dump_json(indent=2))
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from models.evento_model import ConfirmacaoEvento, DetalhesEvento, ExtracaoEvento

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_URL"))

def extrair_informacao_evento(entrada_usuario: str):
    
    hoje = datetime.now()
    contexto_data = f"Hoje é {hoje.strftime('%A, %d de %B de %Y')}"
    
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input=f"{contexto_data} analise se o texto descreve um evento de calendario.",
        instructions=f"Extraia informações sobre um possível evento deste texto: '{entrada_usuario}'",
        text_format=ExtracaoEvento
    )

    return response.output_parsed


def analisar_detalhes_evento(descricao: str) -> DetalhesEvento:
    
    hoje = datetime.now()
    contexto_data = f"Hoje é {hoje.strftime('%A, %d de %B de %Y')}"
    
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input=f"""{contexto_data} extraia informações detalhadas do evento. 
        Quando as datas fizerem referência a 'próxima terça-feira' ou datas relativas similares, 
        use a data atual como referencia.""",
        instructions=f"Extraia detalhes estruturados deste texto de evento: '{descricao}'",
        text_format=DetalhesEvento
    )

    return response.output_parsed


def gerar_confirmacao(detalhes_evento: DetalhesEvento) -> Optional[ConfirmacaoEvento]:
    
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input="Gere uma mensagem de confirmação natural para o evento. Assine a mensagem com seu nome: Skynet.",
        instructions=f"Crie uma notificação para este evento: '{detalhes_evento.model_dump()}'",
        text_format=ConfirmacaoEvento
    )

    return response.output_parsed


def processar_solicitacao_calendário(entrada_usuario: str) -> Optional[ConfirmacaoEvento]:
    extracao_inicial = extrair_informacao_evento(entrada_usuario)
    
    if (
        not extracao_inicial.eh_evento_calendario
        or extracao_inicial.pontuacao_confianca < 0.7
    ):
        return None
    
    detalhes_evento = analisar_detalhes_evento(extracao_inicial)
    confirmacao = gerar_confirmacao(detalhes_evento)
    
    return confirmacao
    

entrada_usuario = """Vamos fazer uma trasmição ao vivo na 
próxima segunda-feira às 20h com Daniel e Alberto para apresentar
o lançamento do novo curso, deve durar umas 2 horas.
"""

evento = processar_solicitacao_calendário(entrada_usuario)

print(evento.mensagem_confirmacao)
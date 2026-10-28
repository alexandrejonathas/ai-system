import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from models.evento_model import (
    DetalhesModificarEvento,
    DetalhesNovoEvento,
    RespostaCalendario,
    TipoSolicitacaoEvento,
)

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=os.getenv("GROQ_API_URL"))


def rotear_solicitacao_calendario(entrada_usuario: str) -> TipoSolicitacaoEvento:
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input="Determine se esta é uma solicitação para criar um novo evento de calendário ou modificar um existente.",
        instructions=f"Analise esta solicitação: '{entrada_usuario}'",
        text_format=TipoSolicitacaoEvento
    )

    return response.output_parsed


def processar_novo_evento(descricao: str):
    
    hoje = datetime.now()
    contexto_data = f"Hoje é {hoje.strftime('%A, %d de %B de %Y')}"
    
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input=f"{contexto_data} extraia detalhes para criar um novo evento de calendario.",
        instructions=f"Extraia informações estruturadas desta descricao: '{descricao}'",
        text_format=DetalhesNovoEvento
    )

    detalhes = response.output_parsed
    
    return RespostaCalendario(
        sucesso=True,
        mensagem=f"Criar novo evento '{detalhes.nome}' para {detalhes.data} com {', '.join(detalhes.participantes)}",
        link_calendario=f"calendar://new?event={detalhes.nome}"
    )
    
def processar_modificar_evento(descricao: str):
    
    hoje = datetime.now()
    contexto_data = f"Hoje é {hoje.strftime('%A, %d de %B de %Y')}"
    
    response = client.responses.parse(
        model=os.getenv("GROQ_MODEL"),
        input=f"{contexto_data} extraia detalhes para modificar um evento de calendario existente.",
        instructions=f"Extraia informações de modificação desta descricao: '{descricao}'",
        text_format=DetalhesModificarEvento
    )

    detalhes = response.output_parsed
    
    mudancas_texto = ", ".join(
        [f"{m.campo} para {m.novo_valor}" for m in detalhes.mudancas]
    )
    
    return RespostaCalendario(
        sucesso=True,
        mensagem=f"Modificado evento '{detalhes.identificador_evento}': {mudancas_texto}",
        link_calendario=f"calendar://modify?event={detalhes.identificador_evento}"
    )    

def processar_solicitacao_calendario(entrada_usuario: str) -> Optional[RespostaCalendario]:
    resultado_roteamento = rotear_solicitacao_calendario(entrada_usuario)
    
    if resultado_roteamento.pontuacao_confianca < 0.7:
        return None
    
    if resultado_roteamento.tipo_solicitacao == "novo_evento":
        return processar_novo_evento(resultado_roteamento.descricao)
    elif resultado_roteamento.tipo_solicitacao == "modificar_evento":
        return processar_modificar_evento(resultado_roteamento.descricao)
    else:
        return None

entrada_usuario = """Vamos fazer uma trasmição ao vivo na 
próxima segunda-feira às 20h com Daniel e Alberto para apresentar
o lançamento do novo curso, deve durar umas 2 horas.
"""

evento = processar_solicitacao_calendario(entrada_usuario)

if evento:
    print(evento.mensagem)
    
    if evento.link_calendario:
        print(f"Link do evento: {evento.link_calendario}")
else:
    print("Solicitação não reconhecida como operação de calendário")
    
entrada_modificar = "Você pode mover a trasmição ao vivo com Alberto e Daniel para quarta-feira as 19h?"

evento = processar_solicitacao_calendario(entrada_modificar)

if evento:
    print(evento.mensagem)
    
    if evento.link_calendario:
        print(f"Link do evento: {evento.link_calendario}")
else:
    print("Solicitação não reconhecida como operação de calendário")
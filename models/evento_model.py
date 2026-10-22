
from typing import Optional

from pydantic import BaseModel, Field


class ExtracaoEvento(BaseModel):
    
    descricao: str = Field(description="Descrição bruta do evento")
    eh_evento_calendario: bool = Field(
        description="Se este texto descreve um evento de calendário"
    )
    pontuacao_confianca: float = Field(
        description="Pontuacao de confiança entre 0 e 1"
    )

class DetalhesEvento(BaseModel):
    
    nome: str = Field(description="Nome do evento")
    data: str = Field(
        description="Data e hora do evento. Use formato ISO8601 para este valor."
    )
    duracao_minutos: Optional[int] = Field(
        description="Duração esperada em minutos"
    )
    participantes: list[str] = Field(
        description="Lista de participantes"
    )


class ConfirmacaoEvento(BaseModel):
    
    mensagem_confirmacao: str = Field(
        description="Mensagem de confirmação em linguagem natural."
    )
    link_calendario: Optional[str] = Field(
        description="Link do calendário gerado se aplicável"
    )

from typing import Literal, Optional

from pydantic import BaseModel, Field


class TipoSolicitacaoEvento(BaseModel):
    tipo_solicitacao: Literal["novo_evento", "modificar_evento"] = Field(
        description="Tipo de solicitação de evento sendo realizada"
    )
    pontuacao_confianca: float = Field(
        description="Pontuação de confiança entre 0 e 1"
    )
    descricao: str = Field(
        description="Descrição limpa da solicitação"
    )

class ExtracaoEvento(BaseModel):
    descricao: str = Field(description="Descrição bruta do evento")
    eh_evento_calendario: bool = Field(
        description="Se este texto descreve um evento de calendário"
    )
    pontuacao_confianca: float = Field(
        description="Pontuacao de confiança entre 0 e 1"
    )

class DetalhesNovoEvento(BaseModel):
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


class Mudanca(BaseModel):
    campo: str = Field(
        description="Campo a ser alterado"
    )
    novo_valor: str = Field(
        description="Novo valor para o campo"
    )

class DetalhesModificarEvento(BaseModel):
    identificador_evento: str = Field(
        description="Descrição para identificar o evento existente"
    )
    mudancas: list[Mudanca] = Field(
        description="Lista de mudanças a fazer"
    )
    participantes_adicionar: list[str] = Field(
        description="Novos participantes para adicionar"
    )
    partipantes_remover: list[str] = Field(
        description="Participantes para remover"
    )


class RespostaCalendario(BaseModel):
    sucesso: bool = Field(
        description="Se operação foi bem sucedida"
    )
    mensagem: str = Field(
        description="Mensagem de confirmação em linguagem natural."
    )
    link_calendario: Optional[str] = Field(
        description="Link do calendário gerado se aplicável"
    )
    
class ValidacaoCalendario(BaseModel):
    eh_solicitacao_calendario: bool = Field(
        description="Se a entrada parece segura"
    )
    pontuacao_confianca: float = Field(
        description="Pontuação de confiança entre 0 e 1"
    )
    
class VerificacaoSeguranca(BaseModel):
    eh_seguro: bool = Field(
        description="Se a entrada parece segura"
    )
    sinalizadores_risco: list[str] = Field(
        description="Lista de possiveis preocupações de segurança"
    )
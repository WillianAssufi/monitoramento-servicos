from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from datetime import datetime

from app.tipo_verificacao import TipoVerificacao


class ServicoCreate(BaseModel):
    nome: str = Field(min_length=1)
    url: HttpUrl
    intervalo_minutos: int = Field(ge=1)
    ativo: bool = True
    tipo_verificacao: TipoVerificacao = TipoVerificacao.http

class ServicoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1)
    url: HttpUrl | None = None
    intervalo_minutos: int | None = Field(default=None, ge=1)
    ativo: bool | None = None
    tipo_verificacao: TipoVerificacao | None = None

class ServicoOut(BaseModel):
    id: int
    nome: str
    url: str
    intervalo_minutos: int
    ativo: bool
    criado_em: datetime
    tipo_verificacao: TipoVerificacao

    model_config = ConfigDict(from_attributes=True)

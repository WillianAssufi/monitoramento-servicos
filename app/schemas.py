from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime


class ServicoCreate(BaseModel):
    nome: str
    url: HttpUrl
    intervalo_minutos: int
    ativo: bool = True

class ServicoUpdate(BaseModel):
    nome: str | None = None
    url: HttpUrl | None = None
    intervalo_minutos: int | None = None
    ativo: bool | None = None

class ServicoOut(BaseModel):
    id: int
    nome: str
    url: str
    intervalo_minutos: int
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)

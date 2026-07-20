from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, String, text
from datetime import datetime

from app.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(2500))
    intervalo_minutos: Mapped[int] = mapped_column()
    ativo: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())


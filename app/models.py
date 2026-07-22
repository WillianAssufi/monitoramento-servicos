from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, String, text, ForeignKey, DateTime
from datetime import datetime

from app.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(2500))
    intervalo_minutos: Mapped[int] = mapped_column()
    ativo: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ultima_verificacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

class Verificacao(Base):
    __tablename__ = "verificacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    servico_id: Mapped[int] = mapped_column(ForeignKey("servicos.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(10))
    tempo_resposta_ms: Mapped[int | None] = mapped_column()
    codigo_http: Mapped[int | None] = mapped_column()
    verificado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.config import settings

URL_TESTE = settings.database_url_teste

assert "teste" in URL_TESTE, "ABORTADO: a URL de teste precisa apontar pro banco de teste!"

engine_teste = create_engine(URL_TESTE)
SessionTeste = sessionmaker(bind=engine_teste)

URL_ENTRADA = settings.database_url

def garantir_banco_teste():
    engine_entrada = create_engine(URL_ENTRADA, isolation_level="AUTOCOMMIT")
    with engine_entrada.connect() as conn:
        existe = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'monitoramento_servicos_teste'")
        ).scalar()
        if not existe:
            conn.execute(text("CREATE DATABASE monitoramento_servicos_teste"))
    engine_entrada.dispose()

@pytest.fixture(scope="session", autouse=True)
def preparar_banco_teste():
    garantir_banco_teste()
    yield

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine_teste)
    sessao = SessionTeste()
    try:
        yield sessao
    finally:
        sessao.close()
        Base.metadata.drop_all(bind=engine_teste)

@pytest.fixture
def client(db):
    def get_db_de_teste():
        yield db

    app.dependency_overrides[get_db] = get_db_de_teste
    yield TestClient(app)
    app.dependency_overrides.clear()
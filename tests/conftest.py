import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.config import settings

URL_TESTE = settings.database_url_teste

assert "teste" in URL_TESTE, "ABORTADO: a URL de teste precisa apontar pro banco de teste!"

engine_teste = create_engine(URL_TESTE)
SessionTeste = sessionmaker(bind=engine_teste)

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
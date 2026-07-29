from app.models import Verificacao

def test_criar_servico(client):
    resposta = client.post("/servicos", json={
        "nome": "Google",
        "url": "https://google.com/",
        "intervalo_minutos": 5,
    })

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Google"
    assert resposta.json()["id"] is not None
    
def test_criar_servico_url_invalida(client):
    resposta = client.post("/servicos", json={
            "nome": "Não existe",
            "url": "SiteQueNaoExiste",
            "intervalo_minutos": 5,
        })
    
    assert resposta.status_code == 422
    
def test_atualizar_servico(client):
    novo_servico = client.post("/servicos", json={
            "nome": "Google",
            "url": "https://google.com/",
            "intervalo_minutos": 5,
        })
    servico_id = novo_servico.json()["id"]  
    
    resposta = client.patch(f"/servicos/{servico_id}", json={
            "nome": "Instagram",
            "url": "https://instagram.com/",
            "intervalo_minutos": 2,
            "ativo": False
    })

    assert resposta.status_code == 200
    assert resposta.json()["id"] is not None
    assert resposta.json()["nome"] == "Instagram"
    assert resposta.json()["url"] == "https://instagram.com/"
    assert resposta.json()["intervalo_minutos"] == 2
    assert resposta.json()["ativo"] is False
    
def test_atualizar_servico_url_invalida(client):
    novo_servico = client.post("/servicos", json={
                "nome": "Google",
                "url": "https://google.com/",
                "intervalo_minutos": 5,
            })
    servico_id = novo_servico.json()["id"]   
    
    resposta = client.patch(f"/servicos/{servico_id}", json={
                "nome": "Goole",
                "url": "SiteQueNaoExiste",
                "intervalo_minutos": 5,
            })
        
    assert resposta.status_code == 422

def test_listar_servicos_vazio(client):
    resposta = client.get("/servicos")
    assert resposta.status_code == 200
    assert resposta.json() == []  

def test_listar_servicos(client):
    novo_servico = client.post("/servicos", json={
                    "nome": "Google",
                    "url": "https://google.com/",
                    "intervalo_minutos": 5,
                })

    resposta = client.get("/servicos")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert len(dados) == 1
    assert dados[0]["nome"] == "Google"
    assert dados[0]["url"] == "https://google.com/"
    assert dados[0]["intervalo_minutos"] == 5
    assert dados[0]["ativo"] is True

def test_buscar_servico(client):
    novo_servico = client.post("/servicos", json={
                        "nome": "Google",
                        "url": "https://google.com/",
                        "intervalo_minutos": 5,
                    })
    servico_id = novo_servico.json()["id"]

    resposta = client.get(f"/servicos/{servico_id}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] is not None


def test_buscar_servico_inexistente(client):
    resposta = client.get(f"/servicos/{999}")

    assert resposta.status_code == 404

def test_deletar_servico(client):
    novo_servico = client.post("/servicos", json={
                            "nome": "Google",
                            "url": "https://google.com/",
                            "intervalo_minutos": 5,
                        })
    servico_id = novo_servico.json()["id"]

    resposta = client.delete(f"/servicos/{servico_id}")

    assert resposta.status_code == 204

    busca = client.get(f"/servicos/{servico_id}")

    assert busca.status_code == 404

def test_deletar_servico_inexistente(client):
    resposta = client.delete(f"/servicos/{999}")

    assert resposta.status_code == 404

def test_verificar_metrica_inexistente(client):
    novo_servico = client.post("/servicos", json={
                                "nome": "Google",
                                "url": "https://google.com/",
                                "intervalo_minutos": 5,
                            })
    servico_id = novo_servico.json()["id"]

    resposta = client.get(f"/servicos/{servico_id}/metricas")

    assert resposta.json()["mensagem"] == "sem verificações ainda"
    assert resposta.json()["uptime %"] is None

def test_metricas(client, db):
    novo_servico = client.post("/servicos", json={
                                    "nome": "Google",
                                    "url": "https://google.com/",
                                    "intervalo_minutos": 5,
                                })
    servico_id = novo_servico.json()["id"]

    db.add(Verificacao(servico_id=servico_id, status="UP", tempo_resposta_ms=100, codigo_http=200))
    db.add(Verificacao(servico_id=servico_id, status="UP", tempo_resposta_ms=200, codigo_http=200))
    db.add(Verificacao(servico_id=servico_id, status="DOWN", tempo_resposta_ms=None, codigo_http=None))
    db.commit()

    resposta = client.get(f"/servicos/{servico_id}/metricas")

    assert resposta.json()["uptime %"] == 66.67
    assert resposta.json()["tempo_medio"] == 150
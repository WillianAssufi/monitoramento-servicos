

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

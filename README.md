# Watchdog — API de Monitoramento de Serviços

API que monitora a saúde de serviços web: você cadastra URLs, o sistema verifica a disponibilidade periodicamente, registra o histórico de cada verificação e acompanha incidentes (quedas e recuperações).

> **Projeto em desenvolvimento ativo** — construído passo a passo como estudo aprofundado de backend, infraestrutura e observabilidade.

## Stack

| Camada | Tecnologia |
|---|---|
| API | Python 3.14 · FastAPI · Uvicorn |
| Banco de dados | PostgreSQL 18 (Docker) |
| ORM / Migrations | SQLAlchemy 2.0 · Alembic |
| Verificações HTTP | httpx |
| Agendamento | APScheduler |
| Configuração | pydantic-settings + `.env` |
| Gerenciador de projeto | uv |
| Infraestrutura | Docker Compose |

**No roadmap:** Playwright (verificação de renderização) · Grafana (dashboards de uptime) · Robot Framework (testes automatizados)

## Progresso

- [x] PostgreSQL 18 em container com volume persistente
- [x] Configuração segura via `.env` + pydantic-settings (zero segredos no código)
- [x] Conexão SQLAlchemy 2.0 (sintaxe moderna `Mapped` / `mapped_column`)
- [x] Migrations versionadas com Alembic
- [x] Modelo de serviços monitorados
- [x] CRUD completo de serviços (POST, GET, PATCH, DELETE)
- [x] Verificador HTTP (status up/down, latência, código HTTP)
- [x] Histórico de verificações persistido
- [x] Scheduler autônomo (verifica cada serviço no seu próprio intervalo)
- [x] Timestamps em UTC (`timestamptz`)
- [ ] Registro de incidentes (início/fim de indisponibilidade)
- [ ] Métricas de uptime e tempo médio de resposta
- [ ] Dashboard no Grafana
- [ ] Testes automatizados
- [ ] Containerização completa da aplicação

## Como rodar

Pré-requisitos: [Docker](https://www.docker.com/) e [uv](https://docs.astral.sh/uv/)

```bash
# 1. Clone o repositório
git clone https://github.com/WillianAssufi/monitoramento-servicos.git
cd monitoramento-servicos

# 2. Configure as variáveis de ambiente
# (copie o exemplo e ajuste usuário/senha)
copy .env.example .env

# 3. Suba o banco de dados
docker compose up -d

# 4. Instale as dependências
uv sync

# 5. Aplique as migrations
uv run alembic upgrade head

# 6. Suba a API
uv run uvicorn app.main:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

## Estrutura do projeto

```
monitoramento-servicos/
├── app/
│   ├── main.py          # aplicação FastAPI + lifespan do scheduler
│   ├── config.py        # settings (lê o .env)
│   ├── database.py      # engine, sessão e Base do SQLAlchemy
│   ├── models.py        # modelos do banco (Servico, Verificacao)
│   ├── schemas.py       # contratos de entrada/saída da API (Pydantic)
│   ├── verificador.py   # verificação HTTP de uma URL (httpx)
│   ├── scheduler.py     # varredura periódica dos serviços vencidos
│   └── routers/
│       └── servicos.py  # CRUD de serviços
├── alembic/
│   └── versions/        # migrations versionadas
├── docker-compose.yml   # PostgreSQL containerizado
└── pyproject.toml       # dependências do projeto
```

## Decisões técnicas

Algumas escolhas conscientes feitas durante o desenvolvimento:

- **API síncrona** — o trabalho pesado (verificar URLs) rodará em um scheduler em segundo plano, não no ciclo request/response. O CRUD da API é leve, então `async` adicionaria complexidade sem resolver um gargalo real.
- **`postgres:18` (major fixada)** — recebe patches de segurança automaticamente sem risco de upgrade de versão maior não intencional.
- **Porta `5433` no host** — permite conviver com uma instalação local de PostgreSQL sem conflito, mapeando para a `5432` interna do container.
- **`server_default` além de `default`** — valores padrão garantidos pelo próprio banco, protegendo até inserções feitas fora do ORM.
- **Segredos centralizados no `.env`** — o `docker-compose.yml` referencia variáveis (`${...}`) em vez de conter credenciais, permitindo repositório público sem vazamento.
- **Scheduler stateless** — em vez de um job por serviço (que se perde em restart e exige sincronização com o CRUD), uma única varredura periódica consulta o banco e decide quem está vencido. A fonte da verdade é sempre o banco.
- **Timestamps em UTC** — colunas `timestamptz` e `datetime.now(timezone.utc)` no código. Armazena-se no fuso universal; a conversão para fuso local é responsabilidade da camada de exibição.
- **Desnormalização consciente** — `ultima_verificacao` vive na tabela de serviços (além do histórico) para que a consulta "quem está vencido?" seja trivial; ambas são atualizadas na mesma transação.
- **Dados honestos** — quando um serviço não responde, `codigo_http` e `tempo_resposta_ms` são gravados como `NULL`, nunca valores inventados. Exceções capturadas de forma específica (`httpx.RequestError`), sem `except` genérico mascarando bugs.

## Autor

**Willian Assufi** — projeto de estudo com foco em backend Python e infraestrutura.

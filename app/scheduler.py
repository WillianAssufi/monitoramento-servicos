from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Servico, Verificacao, Incidente
from app.verificador import verificar_url, verificar_playwright
from app.tipo_verificacao import TipoVerificacao


def verificar_servicos_pendentes():
    with SessionLocal() as db:
        query = select(Servico).where(Servico.ativo == True)
        servicos_ativos = db.execute(query).scalars().all()

        for servico in servicos_ativos:
            if servico.ultima_verificacao is None:
                vencido = True
            else:
                minutos_passados = (datetime.now(timezone.utc) - servico.ultima_verificacao).total_seconds() / 60
                vencido = minutos_passados >= servico.intervalo_minutos - 0.25
            if not vencido:
                continue

            servico.ultima_verificacao = datetime.now(timezone.utc)
            if servico.tipo_verificacao == TipoVerificacao.playwright:
                resultado = verificar_playwright(servico.url)
            else:
                resultado = verificar_url(servico.url)
            
            nova_verificacao = Verificacao(
                servico_id= servico.id,
                status= resultado["status"],
                tempo_resposta_ms= resultado["tempo_resposta_ms"],
                codigo_http= resultado["codigo_http"],
            )
            
            db.add(nova_verificacao)

            query_incidente = select(Incidente).where(Incidente.servico_id == servico.id, Incidente.resolvido_em.is_(None))
            incidente_aberto = db.execute(query_incidente).scalar_one_or_none()

            if resultado["status"] == "DOWN" and incidente_aberto is None:
                incidente_novo = Incidente(
                    servico_id= servico.id
                )
                db.add(incidente_novo)

            if resultado["status"] == "UP" and incidente_aberto is not None:
                incidente_aberto.resolvido_em = datetime.now(timezone.utc)

            db.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(verificar_servicos_pendentes, "interval", seconds=30, next_run_time=datetime.now())
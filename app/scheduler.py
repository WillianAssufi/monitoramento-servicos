from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Servico, Verificacao
from app.verificador import verificar_url


def verificar_servicos_pendentes():
    print("verificando servicos pendentes...")
    with SessionLocal() as db:
        query = select(Servico).where(Servico.ativo == True)
        servicos_ativos = db.execute(query).scalars().all()

        for servico in servicos_ativos:
            if servico.ultima_verificacao is None:
                vencido = True
            else:
                minutos_passados = (datetime.now(timezone.utc) - servico.ultima_verificacao).total_seconds() / 60
                vencido = minutos_passados >= servico.intervalo_minutos
            if not vencido:
                continue

            resultado = verificar_url(servico.url)
            nova_verificacao = Verificacao(
                servico_id= servico.id,
                status= resultado["status"],
                tempo_resposta_ms= resultado["tempo_resposta_ms"],
                codigo_http= resultado["codigo_http"],
            )
            servico.ultima_verificacao = datetime.now(timezone.utc)
        
            db.add(nova_verificacao)
            db.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(verificar_servicos_pendentes, "interval", seconds=30, next_run_time=datetime.now())
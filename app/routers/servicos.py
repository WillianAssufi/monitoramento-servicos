from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Servico
from app.schemas import ServicoCreate, ServicoOut, ServicoUpdate


router = APIRouter(prefix="/servicos", tags=["Serviços"])

@router.post("", response_model=ServicoOut, status_code=201)
def criar_servico(servico: ServicoCreate, db: Session = Depends(get_db)):
    novo_servico = Servico(
        nome=servico.nome,
        url=servico.url,
        intervalo_minutos=servico.intervalo_minutos,
        ativo=servico.ativo,
    )
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico

@router.get("", response_model= list[ServicoOut])
def listar_servicos(db: Session = Depends(get_db)):
    query = select(Servico)
    resultado = db.execute(query)
    servicos = resultado.scalars().all()

    return servicos

@router.get("/{servico_id}", response_model= ServicoOut)
def buscar_servico(servico_id: int, db: Session = Depends(get_db)):
    servico = db.get(Servico, servico_id)
    
    if servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    return servico

@router.patch("/{servico_id}", response_model=ServicoOut)
def atualizar_servico(servico_id: int, servico_update: ServicoUpdate, db: Session = Depends(get_db)):
    servico = db.get(Servico, servico_id)

    if servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    dados = servico_update.model_dump(exclude_unset=True)

    for campo, valor in dados.items():
        setattr(servico, campo, valor)
    
    db.commit()
    db.refresh(servico)

    return servico

@router.delete("/{servico_id}", status_code=204)
def deletar_servico(servico_id: int, db: Session = Depends (get_db)):
    servico = db.get(Servico, servico_id)

    if servico is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    db.delete(servico)
    db.commit()
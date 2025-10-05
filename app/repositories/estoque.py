from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.estoque import EstoqueMovimentoCreate, VendaCreate, DevolucaoCreate, AjusteCreate
from app.models.estoqueMovimento import EstoqueMovimento
from fastapi import HTTPException, status

def create(db: Session, payload: EstoqueMovimentoCreate) -> EstoqueMovimento:
    if payload.tipo == "SAIDA":
        saldo_atual = get_saldo(db=db, produto_id=payload.produto_id)
        if saldo_atual < payload.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Saldo insuficiente em estoque. Saldo Atual: {saldo_atual}, Tentativa de saida: {payload.quantidade}"
            )
    movimento_data = payload.model_dump()
    db_movimento = EstoqueMovimento(**movimento_data)
    db.add(db_movimento)
    db.commit()
    db.refresh(db_movimento)
    
    return db_movimento

def get_saldo(db: Session, produto_id: int) -> int:
    total_entradas = db.query(func.sum(EstoqueMovimento.quantidade)).filter(
        EstoqueMovimento.produto_id == produto_id,
        EstoqueMovimento.tipo == 'ENTRADA'
    ).scalar() or 0
    
    total_saidas = db.query(func.sum(EstoqueMovimento.quantidade)).filter(
        EstoqueMovimento.produto_id == produto_id,
        EstoqueMovimento.tipo == 'SAIDA'
    ).scalar() or 0
    
    saldo = total_entradas - total_saidas
    return saldo

def registrar_venda(db: Session, payload: VendaCreate) -> EstoqueMovimento:
    movimento_payload = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo='SAIDA',
        quantidade=payload.quantidade,
        motivo='venda'
    )
    return create(db=db, payload=movimento_payload)

def registrar_devolucao(db: Session, payload: DevolucaoCreate) -> EstoqueMovimento:
    movimento_payload = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo='ENTRADA',
        quantidade=payload.quantidade,
        motivo='devolução'
    )
    return create(db=db, payload=movimento_payload)

def registrar_ajuste(db: Session, payload: AjusteCreate) -> EstoqueMovimento:
    movimento_payload = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo=payload.tipo,
        quantidade=payload.quantidade,
        motivo=payload.motivo
    )
    return create(db=db, payload=movimento_payload)

def get_extrato_produto_id(db: Session, produto_id: int, offset: int = 0, limit: int = 100) -> list[EstoqueMovimento]:
    extrato = (
        db.query(EstoqueMovimento).filter(EstoqueMovimento.produto_id == produto_id).order_by(EstoqueMovimento.criado_em.desc()).offset(offset).limit(limit).all()
    )
    return extrato



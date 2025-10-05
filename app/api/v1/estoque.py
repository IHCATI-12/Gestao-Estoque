from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.estoque import EstoqueMovimentoCreate, EstoqueMovimentoOut, SaldoOut, VendaCreate, DevolucaoCreate, AjusteCreate, ResumoEstoqueOut
from app.repositories import estoque as repositorio_estoque
from app.repositories import produto as repositorio_produto

rotas = APIRouter(prefix="/v1/estoque", tags=["estoque"])

@rotas.post("/movimentos", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def create(payload: EstoqueMovimentoCreate, db: Session = Depends(get_db)):
    return repositorio_estoque.create(db=db, payload=payload)

@rotas.get("/saldo/{produto_id}", response_model=SaldoOut)
def get_saldo(produto_id: int, db: Session = Depends(get_db)):
    saldo = repositorio_estoque.get_saldo(db=db, produto_id=produto_id)
    return {"produto_id": produto_id, "saldo": saldo}

@rotas.post("/venda", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def realizar_venda(payload: VendaCreate, db: Session = Depends(get_db)):
    return repositorio_estoque.registrar_venda(db=db, payload=payload)

@rotas.post("/devolucao", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def realizar_devolucao(payload: DevolucaoCreate, db: Session = Depends(get_db)):
    return repositorio_estoque.registrar_devolucao(db=db, payload=payload)

@rotas.post("/ajuste", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def realizar_ajuste(payload: AjusteCreate, db: Session = Depends(get_db)):
    return repositorio_estoque.registrar_ajuste(db=db, payload=payload)

@rotas.get("/extrato/{produto_id}", response_model=list[EstoqueMovimentoOut])
def obter_extrato_produto(produto_id: int, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    return repositorio_estoque.get_extrato_produto_id(db=db, produto_id=produto_id, offset=offset, limit=limit)

@rotas.get("/resumo", response_model=list[ResumoEstoqueOut])
def obter_resumo_estoque(db: Session = Depends(get_db)):
    return repositorio_produto.get_resumo_estoque(db=db)


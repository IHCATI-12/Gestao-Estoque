from sqlalchemy.orm import Session
# tabela produto
from app.models.produto import Produto
from app.models.categoria import Categoria
from fastapi import HTTPException
from app.repositories import estoque as repo_estoque
# contrato da API
from app.schemas.produto import ProdutoCreate
from app.schemas.estoque import ResumoEstoqueOut

def create(db: Session, payload: ProdutoCreate) -> Produto:
    # objeto = Produto(nome=payload.nome, preco=payload.preco,Produto_id=payload.Produto_id )
    # ver se categoria existe
    categoria = db.get(Categoria,payload.categoria_id)
    if not categoria:
        raise HTTPException(
            status_code = 400,
            detail="Categoria nao encontrada"
        )
    objeto = Produto(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)

def get_all(db: Session) -> list[Produto]:
    return db.query(Produto).order_by(Produto.id).all()

def list_produtos_abaixo_minimo(db: Session) -> list[Produto]:
    todos_os_produtos = db.query(Produto).filter(Produto.ativo == True).all()
    produtos_abaixo_minimo = []
    
    for produto in todos_os_produtos:
        saldo_atual = repo_estoque.get_saldo(db=db, produto_id=produto.id)
        if saldo_atual < produto.estoque_minimo:
            produtos_abaixo_minimo.append(produto)
    
    return produtos_abaixo_minimo

def get_resumo_estoque(db: Session) -> list[dict]:
    todos_os_produtos = db.query(Produto).filter(Produto.ativo == True).all()
    lista_resumo = []
    
    for produto in todos_os_produtos:
        saldo_atual = repo_estoque.get_saldo(db=db, produto_id=produto.id)
        abaixo_minimo = saldo_atual < produto.estoque_minimo
        
        resumo_produto = {
            "produto_id": produto.id,
            "nome": produto.nome,
            "saldo": saldo_atual,
            "estoque_minimo": produto.estoque_minimo,
            "abaixo_minimo": abaixo_minimo
        }
        
        lista_resumo.append(resumo_produto)
    
    return lista_resumo
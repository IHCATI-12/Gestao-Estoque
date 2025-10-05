from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EstoqueMovimentoCreate(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str] = None
    
class EstoqueMovimentoOut(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str] = None
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)
    
class SaldoOut(BaseModel):
    produto_id: int
    saldo: int
    
class VendaCreate(BaseModel):
    produto_id: int
    quantidade: int
    
class DevolucaoCreate(BaseModel):
    produto_id: int
    quantidade: int
    
class AjusteCreate(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int
    motivo: str
    
class ResumoEstoqueOut(BaseModel):
    produto_id: int
    nome: str
    saldo: int
    estoque_minimo: int
    abaixo_minimo: bool
    model_config = ConfigDict(from_attributes=True)
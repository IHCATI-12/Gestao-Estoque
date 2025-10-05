from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class EstoqueMovimento(Base):
    __tablename__ = "estoque_movimentos"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(
        Integer, 
        ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False
    )
    tipo = Column(String)
    quantidade = Column(Integer)
    motivo = Column(String, nullable=True)
    criado_em = Column(DateTime, server_default=func.now())
    produto = relationship("Produto")
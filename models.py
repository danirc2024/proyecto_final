from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    email = Column(String, primary_key=True)  # Email como clave primaria
    nombre = Column(String, nullable=False)
 #   pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")
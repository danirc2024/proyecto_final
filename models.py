from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    email = Column(String, primary_key=True)  # Email como clave primaria
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'Pedidos'
    
    ID_pedido = Column(Integer, primary_key=True)
    Correo_cliente = Column(String, ForeignKey("clientes.email", ondelete="CASCADE"), nullable=False)  # ForeignKey a clientes.email
    Menu = Column(String, nullable=False)
    Cantidad = Column(Integer, nullable=False)
    
    # Relación inversa con clientes
    cliente = relationship("Cliente", back_populates="pedidos")
    
    

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, REAL, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    email = Column(String, primary_key=True)  # Email como clave primaria
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Pedido(Base):
    __tablename__ = 'Pedidos'
    
    ID_pedido = Column(Integer, primary_key=True, autoincrement=True)
    Correo_cliente = Column(String, ForeignKey("clientes.email", ondelete="CASCADE"), nullable=False)  # ForeignKey a clientes.email
    Menu = Column(String, nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Total = Column(REAL, nullable=False)  # Nuevo campo para el precio total
    Fecha = Column(DateTime, nullable=False)  # Nuevo campo para la fecha del pedido

    
    # Relación inversa con clientes
    cliente = relationship("Cliente", back_populates="pedidos")
    



class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    
    ID_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, unique=True, nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Tipo = Column(String, nullable=False)


class Menu(Base):
    __tablename__ = 'menus'

    ID_menu = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, unique=True, nullable=False)
    Descripcion = Column(String, nullable=False)
    Ingredientes = Column(JSON, nullable=False)  # Lista de ingredientes en formato JSON
    Precio = Column(REAL, nullable=False)  # Precio del menú


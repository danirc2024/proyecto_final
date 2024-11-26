from sqlalchemy.orm import Session
from models import Pedido
from datetime import datetime

class PedidoCRUD:
    @staticmethod
    def crear_pedido(db: Session, correo_cliente: str, menu: str, cantidad: int, total: float):
        """
        Crea un nuevo pedido en la base de datos.
        
        :param db: Sesión de la base de datos.
        :param correo_cliente: Correo del cliente que realiza el pedido.
        :param menu: Menú seleccionado.
        :param cantidad: Cantidad de menús seleccionados.
        :param total: Precio total del pedido.
        :return: El pedido creado o None si ocurre un error.
        """
        try:
            nuevo_pedido = Pedido(
                Correo_cliente=correo_cliente,
                Menu=menu,
                Cantidad=cantidad,
                Total=total,
                Fecha=datetime.now()  # Registrar la fecha actual
            )
            db.add(nuevo_pedido)
            db.commit()
            db.refresh(nuevo_pedido)
            return nuevo_pedido
        except Exception as e:
            db.rollback()
            print(f"Error al crear el pedido: {e}")
            return None

    @staticmethod
    def leer_pedidos(db: Session):
        """
        Obtiene todos los pedidos de la base de datos.
        
        :param db: Sesión de la base de datos.
        :return: Lista de pedidos.
        """
        return db.query(Pedido).all()

    @staticmethod
    def borrar_pedido(db: Session, id_pedido: int):
        """
        Elimina un pedido por su ID.
        
        :param db: Sesión de la base de datos.
        :param id_pedido: ID del pedido a eliminar.
        :return: El pedido eliminado o None si no se encuentra.
        """
        pedido = db.query(Pedido).get(id_pedido)
        if pedido:
            db.delete(pedido)
            db.commit()
            return pedido
        return None
from sqlalchemy.orm import Session
from models import Pedido

class PedidoCRUD:
    @staticmethod
    def leer_pedidos(db: Session):
        """Obtiene todos los pedidos en la base de datos."""
        return db.query(Pedido).all()

    @staticmethod
    def borrar_pedido(db: Session, id_pedido: int):
        """Elimina un pedido de la base de datos por su ID."""
        pedido = db.query(Pedido).get(id_pedido)
        if pedido:
            db.delete(pedido)
            db.commit()
            return pedido
        return None

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Ingrediente

class IngredienteCRUD:
    @staticmethod
    def agregar_ingrediente(db: Session, nombre: str, cantidad: int, tipo: str):
        """Agrega un ingrediente o incrementa la cantidad si ya existe."""
        try:
            # Buscar si el ingrediente ya existe
            ingrediente = db.query(Ingrediente).filter_by(Nombre=nombre).first()
            if ingrediente:
                # Si existe, incrementar la cantidad
                ingrediente.Cantidad += cantidad
            else:
                # Si no existe, crear un nuevo registro
                ingrediente = Ingrediente(Nombre=nombre, Cantidad=cantidad, Tipo=tipo)
                db.add(ingrediente)

            db.commit()
            db.refresh(ingrediente)
            return ingrediente
        except IntegrityError:
            db.rollback()
            return None

    @staticmethod
    def leer_ingredientes(db: Session):
        """Obtiene todos los ingredientes en la base de datos."""
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_ingrediente(db: Session, id_ingrediente: int, nueva_cantidad: int, nuevo_tipo: str = None):
        """Actualiza la cantidad y opcionalmente el tipo de un ingrediente existente."""
        ingrediente = db.query(Ingrediente).get(id_ingrediente)
        if ingrediente:
            ingrediente.Cantidad = nueva_cantidad
            if nuevo_tipo:
                ingrediente.Tipo = nuevo_tipo
            db.commit()
            db.refresh(ingrediente)
            return ingrediente
        return None

    @staticmethod
    def eliminar_ingrediente(db: Session, id_ingrediente: int):
        """Elimina un ingrediente por su ID."""
        ingrediente = db.query(Ingrediente).get(id_ingrediente)
        if ingrediente:
            db.delete(ingrediente)
            db.commit()
            return ingrediente
        return None

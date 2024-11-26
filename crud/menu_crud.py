from sqlalchemy.orm import Session
from models import Menu, Ingrediente
from sqlalchemy.exc import IntegrityError

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, descripcion: str, ingredientes_requeridos: list, precio: float):
        """
        Crea un menú si todos los ingredientes requeridos existen en la base de datos.
        
        :param db: Sesión de la base de datos.
        :param nombre: Nombre del menú.
        :param descripcion: Descripción del menú.
        :param ingredientes_requeridos: Lista de diccionarios con los ingredientes y las cantidades necesarias.
            Ejemplo: [{"nombre": "Harina", "cantidad": 2}, {"nombre": "Huevo", "cantidad": 3}]
        :param precio: Precio del menú.
        :return: El menú creado o None si no se puede crear.
        """
        try:
            # Verificar si todos los ingredientes están disponibles
            for item in ingredientes_requeridos:
                ingrediente = db.query(Ingrediente).filter_by(Nombre=item["nombre"]).first()
                if not ingrediente:
                    return None  # Ingrediente no existe

            # Crear el menú con el precio
            nuevo_menu = Menu(
                Nombre=nombre, 
                Descripcion=descripcion, 
                Ingredientes=ingredientes_requeridos, 
                Precio=precio
            )
            db.add(nuevo_menu)
            db.commit()
            db.refresh(nuevo_menu)
            return nuevo_menu
        except IntegrityError:
            db.rollback()
            return None


    @staticmethod
    def leer_menu_por_nombre(db, nombre_menu):
        """Busca un menú por su nombre en la base de datos."""
        return db.query(Menu).filter_by(Nombre=nombre_menu).first()

    @staticmethod
    def eliminar_menu(db: Session, id_menu: int):
        """
        Elimina un menú por su ID.

        :param db: Sesión de la base de datos.
        :param id_menu: ID del menú a eliminar.
        :return: El menú eliminado o None si no se encuentra.
        """
        menu = db.query(Menu).get(id_menu)
        if menu:
            db.delete(menu)
            db.commit()
            return menu
        return None

    @staticmethod
    def leer_menus(db: Session):
        """
        Obtiene todos los menús disponibles en la base de datos.

        :param db: Sesión de la base de datos.
        :return: Lista de menús.
        """
        return db.query(Menu).all()

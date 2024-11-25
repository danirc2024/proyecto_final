from database import Base, engine
from app import PestañasPrincipal

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app = PestañasPrincipal()
    app.mainloop()

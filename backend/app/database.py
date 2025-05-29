from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://admin_bd:swgahQWq1sW7zkhV2LnUUb1gyd8L9yrQ@dpg-d0s75hs9c44c73crr5v0-a.frankfurt-postgres.render.com/aplicacion_web"

# Motor de conexión
engine = create_engine(DATABASE_URL)

# Creador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

# Dependencia que se usa en los endpoints
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


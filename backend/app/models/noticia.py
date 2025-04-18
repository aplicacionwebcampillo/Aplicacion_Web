from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Noticia(Base):
    __tablename__ = "noticia"

    id_noticia = Column(Integer, primary_key=True)
    titular = Column(String(200), nullable=False, unique=True)
    imagen = Column(String(255))
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False)
    
    administrador = relationship("Administrador", back_populates="noticias")

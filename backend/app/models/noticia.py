from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Noticia(Base):
    __tablename__ = "noticia"

    id_noticia = Column(Integer, primary_key=True)
    titular = Column(String(200), nullable=False, unique=True)
    imagen = Column(String(255))
    contenido = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False)
    dni_administrador = Column(String(9), ForeignKey("administrador.dni"), nullable=True)
    
    administrador = relationship("Administrador", back_populates="noticias")

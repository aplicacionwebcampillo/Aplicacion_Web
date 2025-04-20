from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey

from app.database import Base
from sqlalchemy.orm import relationship

class PostForo(Base):
    __tablename__ = "post_foro"

    id_post = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    moderado = Column(Boolean, default=False)
    tipo = Column(String(20), nullable=False)
    fecha = Column(DateTime)
    dni_usuario = Column(String(9), ForeignKey("usuario.dni"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="posts_foro")

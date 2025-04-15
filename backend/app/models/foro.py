from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class PostForo(Base):
    __tablename__ = "post_foro"

    id_post = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    moderado = Column(Boolean, default=False)
    tipo = Column(String(20), nullable=False)
    fecha = Column(DateTime)


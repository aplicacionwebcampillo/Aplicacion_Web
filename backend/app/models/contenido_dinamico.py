from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base


class ContenidoDinamico(Base):
    __tablename__ = "contenido_dinamico"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    lugar = Column(String, nullable=False)
    orden = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint("tipo IN ('texto', 'imagen')", name="tipo_check"),
    )


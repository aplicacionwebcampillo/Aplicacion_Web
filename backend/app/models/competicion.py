from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Competicion(Base):
    __tablename__ = "competicion"

    nombre = Column(String(100), primary_key=True)
    temporada = Column(String(20), primary_key=True)
    estado = Column(String(20), default='pendiente')
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)

    partidos = relationship("Partido", back_populates="competicion")

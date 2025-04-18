from sqlalchemy import Column, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Partido(Base):
    __tablename__ = "partido"

    nombre_competicion = Column(String(100), primary_key=True)
    temporada_competicion = Column(String(20), primary_key=True)
    local = Column(String(100), primary_key=True)
    visitante = Column(String(100), primary_key=True)
    dia = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    resultado = Column(String(20))
    estadio = Column(String(100))

    competicion = relationship("Competicion", back_populates="partidos")
    predicciones = db.relationship('Predice', back_populates='partido')


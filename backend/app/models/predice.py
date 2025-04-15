from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Predice(Base):
    __tablename__ = "predice"

    dni = Column(String(9), ForeignKey("socio.dni"), primary_key=True)
    nombre_competicion = Column(String(100), primary_key=True)
    temporada_competicion = Column(String(20), primary_key=True)
    local = Column(String(100), primary_key=True)
    visitante = Column(String(100), primary_key=True)
    resultado = Column(String(20), nullable=False)
    pagado = Column(Boolean, default=False)

    socio = relationship("Socio", back_populates="predicciones")

from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.partido import Partido


class Competicion(Base):
    __tablename__ = "competicion"

    nombre = Column(String(100), primary_key=True)
    temporada = Column(String(20), primary_key=True)
    estado = Column(String(20), default='pendiente')
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)

    partidos = relationship(
       "Partido",
       back_populates="competicion",
       foreign_keys="[Partido.nombre_competicion, Partido.temporada_competicion]",
       primaryjoin="and_(Partido.nombre_competicion==Competicion.nombre, Partido.temporada_competicion==Competicion.temporada)"
    )


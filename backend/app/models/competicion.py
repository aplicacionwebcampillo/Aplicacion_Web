from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import CheckConstraint
from app.models.equipo import Equipo
from app.models.clasificacion import Clasificacion
from app.models.partido import Partido

class Competicion(Base):
    __tablename__ = "competicion"

    nombre = Column(String(100), primary_key=True, nullable=False)
    temporada = Column(String(20), primary_key=True, nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo", ondelete="CASCADE"), nullable=False)
    formato = Column(String(20), nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            "formato IN ('Liga', 'Copa')",
            name="competicion_formato_check"
        ),
    )

    equipo = relationship("Equipo", back_populates="competiciones")
    partidos = relationship("Partido", back_populates="competicion")
    clasificacion = relationship("Clasificacion", back_populates="competicion", cascade="all, delete")


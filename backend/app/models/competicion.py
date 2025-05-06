from sqlalchemy import Column, String, Integer, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Competicion(Base):
    __tablename__ = "competicion"

    nombre = Column(String(100), primary_key=True, nullable=False)
    temporada = Column(String(20), primary_key=True, nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "estado IN ('pendiente', 'en_progreso', 'finalizada')",
            name="competicion_estado_check"
        ),
    )
    
    equipo = relationship("Equipo", back_populates="competiciones")
    partidos = relationship("Partido", back_populates="competicion")
    

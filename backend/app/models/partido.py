from sqlalchemy import Column, String, Date, Time, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Partido(Base):
    __tablename__ = 'partido'
    
    nombre_competicion = Column(String(100), nullable=False, primary_key=True)
    temporada_competicion = Column(String(20), nullable=False, primary_key=True)
    local = Column(String(100), nullable=False, primary_key=True)
    visitante = Column(String(100), nullable=False, primary_key=True)
    dia = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    
    jornada = Column(String(50), nullable=False)
    resultado_local = Column(Integer, nullable=True)
    resultado_visitante = Column(Integer, nullable=True)
    acta = Column(String(255), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['nombre_competicion', 'temporada_competicion'],
            ['competicion.nombre', 'competicion.temporada']
        ),
    )

    competicion = relationship("Competicion", back_populates="partidos")
    predicciones = relationship("Predice", back_populates="partido", cascade="all, delete")

    def __repr__(self):
        return f"<Partido {self.local} vs {self.visitante} ({self.dia} {self.hora})>"


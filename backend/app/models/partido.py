from sqlalchemy import Column, String, Date, Time
from sqlalchemy.orm import relationship
from app.database import Base

# Definición del modelo Partido
class Partido(Base):
    __tablename__ = 'partido'
    
    nombre_competicion = Column(String(100), nullable=False, primary_key=True)
    temporada_competicion = Column(String(20), nullable=False, primary_key=True)
    local = Column(String(100), nullable=False, primary_key=True)
    visitante = Column(String(100), nullable=False, primary_key=True)
    dia = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    resultado = Column(String(20), nullable=True)
    estadio = Column(String(100), nullable=True)
    
    competicion = relationship("Competicion", 
                               back_populates="partidos", 
                               foreign_keys=[nombre_competicion, temporada_competicion])
    
    def __repr__(self):
        return f"<Partido {self.local} vs {self.visitante} ({self.dia} {self.hora})>"



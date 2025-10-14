from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    jornada = Column(String(50), nullable=False)
    local = Column(String(100), nullable=False)
    visitante = Column(String(100), nullable=False)
    goles_local = Column(String(10))
    goles_visitante = Column(String(10))
    fecha = Column(String(20))
    hora = Column(String(20))
    categoria = Column(String(50))
    fetched_at = Column(DateTime, default=datetime.utcnow)


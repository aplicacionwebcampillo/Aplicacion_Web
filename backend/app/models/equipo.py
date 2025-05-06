from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Equipo(Base):
    __tablename__ = "equipo"

    id_equipo = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(50), nullable=False)
    num_jugadores = Column(Integer, nullable=False, default=0)

    jugadores = relationship("Jugador", back_populates="equipo", cascade="all, delete-orphan")


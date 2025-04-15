from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Jugador(Base):
    __tablename__ = "jugador"

    id_jugador = Column(Integer, primary_key=True)
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo", ondelete="SET NULL"), nullable=False)
    nombre = Column(String(100), nullable=False)
    posicion = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    foto = Column(String(255))
    biografia = Column(Text)

    equipo = relationship("Equipo", back_populates="jugadores")

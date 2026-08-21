from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Jugador(Base):
    __tablename__ = "jugador"
    id_jugador = Column(Integer, primary_key=True, autoincrement=True)
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo", ondelete="SET NULL"), nullable=False)
    nombre = Column(String(100), nullable=False)
    posicion = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    foto = Column(String(255))
    biografia = Column(Text)
    dorsal = Column(Integer, nullable=False)

    # Enriquecimiento desde lapreferente.com (nombre corto/legal tal y como
    # los distingue esa web, y si la última novedad fue fichaje o renovación).
    nombre_corto = Column(String(100), nullable=True)
    nombre_completo = Column(String(150), nullable=True)
    estado_fichaje = Column(String(30), nullable=True)

    # Estadísticas de la temporada en curso. partidos_jugados y goles se
    # actualizan automáticamente desde la RFAF tras cada jornada; el resto
    # (titularidades, minutos, tarjetas) solo lapreferente.com los publica,
    # así que se actualizan a mano con ese script.
    partidos_jugados = Column(Integer, nullable=False, default=0)
    partidos_titular = Column(Integer, nullable=False, default=0)
    minutos = Column(Integer, nullable=False, default=0)
    goles = Column(Integer, nullable=False, default=0)
    tarjetas_amarillas = Column(Integer, nullable=False, default=0)
    tarjetas_rojas = Column(Integer, nullable=False, default=0)

    equipo = relationship("Equipo", back_populates="jugadores")


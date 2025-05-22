from sqlalchemy import Column, String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Clasificacion(Base):
    __tablename__ = "clasificacion"

    nombre_competicion = Column(String(100), primary_key=True, nullable=False)
    temporada_competicion = Column(String(20), primary_key=True, nullable=False)
    equipo = Column(String(100), primary_key=True, nullable=False)
    posicion = Column(Integer, nullable=False)
    puntos = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["nombre_competicion", "temporada_competicion"],
            ["competicion.nombre", "competicion.temporada"],
            ondelete="CASCADE",
            name="clasificacion_competicion_fkey"
        ),
    )

    competicion = relationship("Competicion", back_populates="clasificacion")

    def __repr__(self):
        return f"<Clasificacion {self.equipo} en {self.nombre_competicion} ({self.temporada_competicion}) - Posición {self.posicion} - {self.puntos} puntos>"


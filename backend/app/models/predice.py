from sqlalchemy import Column, String, Boolean, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Predice(Base):
    __tablename__ = "predice"

    dni = Column(String(9), primary_key=True, nullable=False)
    nombre_competicion = Column(String(100), primary_key=True, nullable=False)
    temporada_competicion = Column(String(20), primary_key=True, nullable=False)
    local = Column(String(100), primary_key=True, nullable=False)
    visitante = Column(String(100), primary_key=True, nullable=False)
    resultado_local = Column(Integer, primary_key=True, nullable=False)
    resultado_visitante = Column(Integer, primary_key=True, nullable=False)
    pagado = Column(Boolean, default=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["dni"],
            ["socio.dni"],
            name="predice_dni_fkey"
        ),
        ForeignKeyConstraint(
            ["nombre_competicion", "temporada_competicion", "local", "visitante"],
            ["partido.nombre_competicion", "partido.temporada_competicion", "partido.local", "partido.visitante"],
            ondelete="CASCADE",
            name="predice_partido_fkey"
        ),
    )

    socio = relationship("Socio", back_populates="predicciones")
    partido = relationship("Partido", back_populates="predicciones")

    def __repr__(self):
        return f"<Predice {self.dni} predice {self.resultado_local}-{self.resultado_visitante} para {self.local} vs {self.visitante}>"


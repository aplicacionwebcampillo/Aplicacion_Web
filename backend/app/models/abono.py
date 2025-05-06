from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Abono(Base):
    __tablename__ = "abono"

    id_abono = Column(Integer, primary_key=True, index=True)
    temporada = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    socios_abonados = relationship("SocioAbono", back_populates="abono")
    cesiones = relationship("CesionAbono", back_populates="abono")


from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Abono(Base):
    __tablename__ = "abono"

    id_abono = Column(Integer, primary_key=True)
    temporada = Column(String(20), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    cesiones = relationship("CesionAbono", back_populates="abono")
    socio_abonos = relationship("SocioAbono", back_populates="abono")

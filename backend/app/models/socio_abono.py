from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SocioAbono(Base):
    __tablename__ = "socio_abono"

    dni = Column(String(9), ForeignKey("socio.dni"), primary_key=True)
    id_abono = Column(Integer, ForeignKey("abono.id_abono"), primary_key=True)
    fecha_compra = Column(Date, nullable=False)
    pagado = Column(Boolean, default=False)

    socio = relationship("Socio", back_populates="socio_abonos")
    abono = relationship("Abono", back_populates="socios_abonados")


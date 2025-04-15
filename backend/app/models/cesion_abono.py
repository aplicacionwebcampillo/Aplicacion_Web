from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CesionAbono(Base):
    __tablename__ = "cesion_abono"

    id_cesion = Column(Integer, primary_key=True)
    dni_cedente = Column(String(9), ForeignKey("socio.dni"), nullable=False)
    dni_beneficiario = Column(String(9), ForeignKey("socio.dni"), nullable=False)
    id_abono = Column(Integer, ForeignKey("abono.id_abono"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_cesion = Column(Date)

    cedente = relationship("Socio", foreign_keys=[dni_cedente], back_populates="cesiones_cedidas")
    beneficiario = relationship("Socio", foreign_keys=[dni_beneficiario], back_populates="cesiones_recibidas")
    abono = relationship("Abono", back_populates="cesiones")

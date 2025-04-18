from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Patrocinador(Base):
    __tablename__ = "patrocinador"

    id_patrocinador = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    email = Column(String(100))
    telefono = Column(String(15))
    logo = Column(String(255), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    
    administrador = relationship("Administrador", back_populates="patrocinadores")

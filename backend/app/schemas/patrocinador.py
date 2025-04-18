from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatrocinadorBase(BaseModel):
    nombre: str
    tipo: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    logo: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class PatrocinadorCreate(PatrocinadorBase):
    dni_administrador: str

class PatrocinadorRead(PatrocinadorBase):
    id_patrocinador: int


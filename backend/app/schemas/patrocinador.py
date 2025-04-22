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


class PatrocinadorUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    logo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    dni_administrador: Optional[str] = None

class PatrocinadorResponse(PatrocinadorBase):
    class Config:
        orm_mode = True


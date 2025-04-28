from pydantic import BaseModel
from typing import Optional
from datetime import date

class JugadorBase(BaseModel):
    id_equipo: int
    nombre: str
    posicion: str
    fecha_nacimiento: date
    foto: Optional[str] = None
    biografia: Optional[str] = None
    dorsal: int

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(BaseModel):
    id_equipo: Optional[int] = None
    nombre: Optional[str] = None
    posicion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    foto: Optional[str] = None
    biografia: Optional[date] = None
    dorsal: Optional[int] = None

class JugadorResponse(JugadorBase):
    class Config:
        orm_mode = True


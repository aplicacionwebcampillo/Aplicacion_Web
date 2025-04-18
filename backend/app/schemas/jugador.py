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

class JugadorCreate(JugadorBase):
    pass

class JugadorRead(JugadorBase):
    id_jugador: int


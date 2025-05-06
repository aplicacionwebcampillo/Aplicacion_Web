from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class JugadorBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    posicion: str = Field(..., max_length=50)
    fecha_nacimiento: date
    foto: Optional[str] = None
    biografia: Optional[str] = None
    dorsal: int
    id_equipo: int


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    posicion: Optional[str] = Field(None, max_length=50)
    fecha_nacimiento: Optional[date] = None
    foto: Optional[str] = None
    biografia: Optional[str] = None
    dorsal: Optional[int] = None
    id_equipo: Optional[int] = None


class JugadorResponse(JugadorBase):
    id_jugador: int

    class Config:
        orm_mode = True


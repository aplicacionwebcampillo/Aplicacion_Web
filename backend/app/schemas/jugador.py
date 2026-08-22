from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class JugadorBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    posicion: str = Field(..., max_length=50)
    fecha_nacimiento: Optional[date] = None
    foto: Optional[str] = None
    biografia: Optional[str] = None
    dorsal: int
    id_equipo: int
    nombre_corto: Optional[str] = Field(None, max_length=100)
    nombre_completo: Optional[str] = Field(None, max_length=150)
    estado_fichaje: Optional[str] = Field(None, max_length=30)
    partidos_jugados: int = 0
    partidos_titular: int = 0
    goles: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0


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
    nombre_corto: Optional[str] = Field(None, max_length=100)
    nombre_completo: Optional[str] = Field(None, max_length=150)
    estado_fichaje: Optional[str] = Field(None, max_length=30)
    partidos_jugados: Optional[int] = None
    partidos_titular: Optional[int] = None
    goles: Optional[int] = None
    tarjetas_amarillas: Optional[int] = None
    tarjetas_rojas: Optional[int] = None


class JugadorResponse(JugadorBase):
    id_jugador: int

    class Config:
        orm_mode = True

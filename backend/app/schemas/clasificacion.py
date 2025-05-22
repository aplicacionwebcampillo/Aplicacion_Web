from pydantic import BaseModel, Field
from typing import Optional


class ClasificacionBase(BaseModel):
    nombre_competicion: str = Field(..., max_length=100)
    temporada_competicion: str = Field(..., max_length=20)
    equipo: str = Field(..., max_length=100)
    posicion: int
    puntos: int


class ClasificacionCreate(ClasificacionBase):
    pass


class ClasificacionUpdate(BaseModel):
    posicion: Optional[int] = None
    puntos: Optional[int] = None


class ClasificacionResponse(ClasificacionBase):
    class Config:
        from_attributes = True 


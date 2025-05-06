from pydantic import BaseModel
from typing import Optional

class EquipoBase(BaseModel):
    categoria: str
    num_jugadores: int = 0

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(BaseModel):
    categoria: Optional[str]
    num_jugadores: Optional[int]

class EquipoResponse(EquipoBase):
    id_equipo: int

    class Config:
        orm_mode = True


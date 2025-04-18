from pydantic import BaseModel

class EquipoBase(BaseModel):
    categoria: str
    num_jugadores: int

class EquipoCreate(EquipoBase):
    pass

class EquipoRead(EquipoBase):
    id_equipo: int


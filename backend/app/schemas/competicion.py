from pydantic import BaseModel, Field, constr
from datetime import date
from typing import Optional
from typing_extensions import Literal

class CompeticionBase(BaseModel):
    nombre: constr(max_length=100)
    temporada: constr(max_length=20)
    estado: Optional[Literal['pendiente', 'en_progreso', 'finalizada']] = 'pendiente'
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    id_equipo: int


class CompeticionCreate(CompeticionBase):
    pass


class CompeticionUpdate(BaseModel):
    estado: Optional[Literal['pendiente', 'en_progreso', 'finalizada']] = 'pendiente'
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_equipo: Optional[int] = None


class CompeticionResponse(CompeticionBase):
    class Config:
        orm_mode = True


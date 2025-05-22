from pydantic import BaseModel, constr
from typing import Optional
from typing_extensions import Literal

class CompeticionBase(BaseModel):
    nombre: constr(max_length=100)
    temporada: constr(max_length=20)
    formato: Literal['Liga', 'Copa']
    id_equipo: int


class CompeticionCreate(CompeticionBase):
    pass


class CompeticionUpdate(BaseModel):
    formato: Optional[Literal['Liga', 'Copa']] = None
    id_equipo: Optional[int] = None


class CompeticionResponse(CompeticionBase):
    class Config:
        orm_mode = True


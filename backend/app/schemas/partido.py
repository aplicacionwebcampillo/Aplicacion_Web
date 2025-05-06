from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class PartidoBase(BaseModel):
    nombre_competicion: str
    temporada_competicion: str
    local: str
    visitante: str
    dia: Optional[date] = None
    hora: Optional[time] = None
    resultado: Optional[str] = None
    estadio: Optional[str] = None

    class Config:
        orm_mode = True

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(PartidoBase):
    dia: Optional[date] = None
    hora: Optional[time] = None
    resultado: Optional[str] = None
    estadio: Optional[str] = None

class PartidoResponse(PartidoBase):
    class Config:
        orm_mode = True


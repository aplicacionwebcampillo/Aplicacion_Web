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
    jornada: str
    resultado_local: Optional[int] = None
    resultado_visitante: Optional[int] = None
    acta: Optional[str] = None

    class Config:
        orm_mode = True

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(BaseModel):
    dia: Optional[date] = None
    hora: Optional[time] = None
    jornada: Optional[str] = None
    resultado_local: Optional[int] = None
    resultado_visitante: Optional[int] = None
    acta: Optional[str] = None

    class Config:
        orm_mode = True

class PartidoResponse(PartidoBase):
    class Config:
        orm_mode = True


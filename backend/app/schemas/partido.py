from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PartidoBase(BaseModel):
    nombre_competicion: str
    temporada_competicion: str
    local: str
    visitante: str
    dia: date
    hora: time
    resultado: Optional[str] = None
    estadio: Optional[str] = None

class PartidoCreate(PartidoBase):
    pass

class PartidoRead(PartidoBase):
    pass


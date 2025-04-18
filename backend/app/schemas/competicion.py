from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompeticionBase(BaseModel):
    nombre: str
    temporada: str
    estado: Optional[str] = "pendiente"
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class CompeticionCreate(CompeticionBase):
    pass

class CompeticionRead(CompeticionBase):
    pass


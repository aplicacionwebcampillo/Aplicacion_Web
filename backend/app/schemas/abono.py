from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class AbonoBase(BaseModel):
    temporada: str
    precio: float
    fecha_inicio: date
    fecha_fin: date

class AbonoCreate(AbonoBase):
    pass

class AbonoUpdate(BaseModel):
    temporada: Optional[str] = None
    precio: Optional[float] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class AbonoResponse(AbonoBase):
    id_abono: int

    class Config:
        orm_mode = True


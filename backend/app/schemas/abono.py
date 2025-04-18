from pydantic import BaseModel
from datetime import date

class AbonoBase(BaseModel):
    temporada: str
    precio: float
    fecha_inicio: date
    fecha_fin: date

class AbonoCreate(AbonoBase):
    pass

class AbonoRead(AbonoBase):
    id_abono: int


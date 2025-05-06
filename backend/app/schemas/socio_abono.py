from pydantic import BaseModel
from datetime import date
from typing import Optional

class SocioAbonoBase(BaseModel):
    dni: str
    id_abono: int
    fecha_compra: date
    pagado: bool = False

class SocioAbonoCreate(SocioAbonoBase):
    pass

class SocioAbonoUpdate(BaseModel):
    fecha_compra: Optional[date] = None
    pagado: Optional[bool] = None

class SocioAbonoResponse(SocioAbonoBase):
    class Config:
        orm_mode = True


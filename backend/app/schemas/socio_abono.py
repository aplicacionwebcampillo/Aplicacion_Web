from pydantic import BaseModel
from typing import Optional
from datetime import date

class SocioAbonoBase(BaseModel):
    dni: str
    id_abono: int
    fecha_compra: Optional[date] = None
    pagado: Optional[bool] = False

class SocioAbonoCreate(SocioAbonoBase):
    pass

class SocioAbonoRead(SocioAbonoBase):
    pass


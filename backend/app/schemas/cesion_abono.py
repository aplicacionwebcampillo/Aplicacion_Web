from pydantic import BaseModel
from typing import Optional
from datetime import date

class CesionAbonoBase(BaseModel):
    dni_cedente: str
    dni_beneficiario: str
    id_abono: int
    fecha_inicio: date
    fecha_fin: date
    fecha_cesion: date

class CesionAbonoCreate(CesionAbonoBase):
    pass

class CesionAbonoUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    fecha_cesion: Optional[date] = None
    dni_beneficiario: Optional[str] = None
    id_abono: Optional[int] = None

class CesionAbonoResponse(CesionAbonoBase):
    id_cesion: int

    class Config:
        orm_mode = True


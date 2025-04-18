from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CesionAbonoBase(BaseModel):
    dni_cedente: str
    dni_beneficiario: str
    id_abono: int
    fecha_inicio: date
    fecha_fin: date
    fecha_cesion: Optional[datetime] = None

class CesionAbonoCreate(CesionAbonoBase):
    pass

class CesionAbonoRead(CesionAbonoBase):
    id_cesion: int


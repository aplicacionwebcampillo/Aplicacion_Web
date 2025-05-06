from pydantic import BaseModel, Field
from typing import Optional


class PrediceBase(BaseModel):
    dni: str = Field(..., max_length=9)
    nombre_competicion: str = Field(..., max_length=100)
    temporada_competicion: str = Field(..., max_length=20)
    local: str = Field(..., max_length=100)
    visitante: str = Field(..., max_length=100)
    resultado: str = Field(..., max_length=20)
    pagado: Optional[bool] = False


class PrediceCreate(PrediceBase):
    pass


class PrediceUpdate(BaseModel):
    resultado: Optional[str] = Field(None, max_length=20)
    pagado: Optional[bool] = None


class PrediceResponse(PrediceBase):
    class Config:
        from_attributes = True  # pydantic v2+


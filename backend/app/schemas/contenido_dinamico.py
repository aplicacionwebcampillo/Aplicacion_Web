from pydantic import BaseModel, Field
from typing import Literal, Optional


class ContenidoBase(BaseModel):
    tipo: Literal["texto", "imagen"]
    contenido: str
    lugar: str
    orden: Optional[int] = 0


class ContenidoCreate(ContenidoBase):
    pass


class ContenidoUpdate(BaseModel):
    tipo: Optional[Literal["texto", "imagen"]] = None
    contenido: Optional[str] = None
    lugar: Optional[str] = None
    orden: Optional[int] = None


class ContenidoResponse(ContenidoBase):
    id: int
    class Config:
        orm_mode = True


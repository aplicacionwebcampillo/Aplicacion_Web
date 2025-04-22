from pydantic import BaseModel
from typing import Optional

class NoticiaBase(BaseModel):
    titular: str
    imagen: Optional[str] = None
    contenido: str
    categoria: str
    dni_administrador: str

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaUpdate(BaseModel):
    titular: Optional[str] = None
    imagen: Optional[str] = None
    contenido: Optional[str] = None
    categoria: Optional[str] = None
    dni_administrador: Optional[str] = None

class NoticiaResponse(NoticiaBase):
    class Config:
        orm_mode = True


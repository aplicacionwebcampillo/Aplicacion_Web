from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostForoBase(BaseModel):
    contenido: str
    tipo: str
    moderado: Optional[bool] = False
    fecha: Optional[datetime] = None
    dni_usuario: str

class PostForoCreate(PostForoBase):
    pass

class PostForoUpdate(BaseModel):
    contenido: Optional[str] = None
    tipo: Optional[str] = None
    moderado: Optional[bool] = False
    fecha: Optional[datetime] = None

class PostForoResponse(PostForoBase):
    class Config:
        orm_mode = True


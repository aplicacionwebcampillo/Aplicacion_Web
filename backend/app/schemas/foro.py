from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostForoBase(BaseModel):
    contenido: str
    tipo: str
    moderado: Optional[bool] = False
    fecha: Optional[datetime] = None
    dni_socio: str

class PostForoCreate(PostForoBase):
    pass

class PostForoRead(PostForoBase):
    id_post: int


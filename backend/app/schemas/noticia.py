from pydantic import BaseModel
from typing import Optional

class NoticiaBase(BaseModel):
    titular: str
    imagen: Optional[str] = None
    contenido: str
    categoria: str

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaRead(NoticiaBase):
    id_noticia: int


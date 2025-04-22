from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    imagen: str

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    imagen: Optional[str] = None

class ProductoResponse(ProductoBase):
    class Config:
        orm_mode = True


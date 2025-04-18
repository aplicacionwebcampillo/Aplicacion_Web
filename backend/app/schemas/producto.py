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

class ProductoRead(ProductoBase):
    id_producto: int


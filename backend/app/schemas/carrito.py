from pydantic import BaseModel
from typing import List, Optional

class ProductoEnCarrito(BaseModel):
    id_producto: int
    nombre: str
    precio: float
    cantidad: int
    subtotal: float

    class Config:
        from_attributes = True

class CarritoDetalle(BaseModel):
    productos: List[ProductoEnCarrito]
    precio_total: float
    descuento: float
    precio_final: float

    class Config:
        from_attributes = True

class AgregarProducto(BaseModel):
    id_producto: int
    cantidad: int

class ActualizarCantidad(BaseModel):
    cantidad: int

class AplicarDescuento(BaseModel):
    codigo: str


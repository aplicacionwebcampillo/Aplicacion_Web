from pydantic import BaseModel
from datetime import date
from typing import Optional, List
# from app.schemas.pedido import PedidoResponse  # incluir pedido

class CompraBase(BaseModel):
    dni: str
    id_pedido: int
    fecha_compra: Optional[date] = None
    pagado: bool = False

class ProductoCompra(BaseModel):
    id_producto: int
    cantidad: int
    talla: str

class CompraCreate(CompraBase):
    productos: List[ProductoCompra]

class CompraUpdate(BaseModel):
    pagado: bool 

class CompraResponse(CompraBase):
    # pedido: Optional[PedidoResponse] = None  # incluir el pedido

    class Config:
        orm_mode = True 


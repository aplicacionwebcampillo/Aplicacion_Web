from pydantic import BaseModel
from typing import List
from typing import Optional
from app.schemas.producto import ProductoResponse


class PedidoBase(BaseModel):
    descuento: float
    precio_total: float

class PedidoCreate(PedidoBase):
    productos_ids: List[int]

class PedidoUpdate(PedidoBase):
    descuento: Optional[float] = None
    precio_total: Optional[float] = None
    productos_ids: Optional[List[int]] = None
    
class PedidoResponse(BaseModel):
    id_pedido: int
    descuento: float
    precio_total: float
    productos: List[ProductoResponse]

    class Config:
        orm_mode = True




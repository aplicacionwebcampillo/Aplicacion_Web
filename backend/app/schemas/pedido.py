from pydantic import BaseModel
from typing import Optional

class PedidoBase(BaseModel):
    descuento: Optional[float] = 0.0
    precio_total: float
    cantidad: Optional[int] = 1

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id_pedido: int


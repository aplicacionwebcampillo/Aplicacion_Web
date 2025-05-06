from pydantic import BaseModel
from datetime import date
from typing import Optional
# from app.schemas.pedido import PedidoResponse  # incluir pedido

class CompraBase(BaseModel):
    dni: str
    id_pedido: int
    fecha_compra: Optional[date] = None
    pagado: bool = False

class CompraCreate(CompraBase):
    pass

class CompraUpdate(BaseModel):
    pagado: bool 

class CompraResponse(CompraBase):
    # pedido: Optional[PedidoResponse] = None  # incluir el pedido

    class Config:
        orm_mode = True 


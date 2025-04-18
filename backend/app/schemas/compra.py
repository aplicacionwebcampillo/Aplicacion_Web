from pydantic import BaseModel
from datetime import date
from typing import Optional

class CompraBase(BaseModel):
    dni: str
    id_pedido: int
    fecha_compra: Optional[date] = None
    pagado: Optional[bool] = False

class CompraCreate(CompraBase):
    pass

class CompraRead(CompraBase):
    pass


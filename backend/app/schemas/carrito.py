from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal

class CarritoItemBase(BaseModel):
    producto_id: int
    nombre: str
    precio_unitario: Decimal
    cantidad: int
    subtotal: Decimal

    class Config:
        orm_mode = True


class CarritoAgregarInput(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0, description="Cantidad debe ser mayor que 0")


class CarritoActualizarInput(BaseModel):
    producto_id: int
    nueva_cantidad: int = Field(..., ge=0, description="Cantidad debe ser 0 o mayor")


class AplicarDescuentoInput(BaseModel):
    codigo: str


class CarritoResponse(BaseModel):
    items: List[CarritoItemBase]
    subtotal: Decimal
    descuento_aplicado: Optional[str] = None
    total: Decimal


class ConfirmacionPedidoResponse(BaseModel):
    mensaje: str
    id_pedido: int
    total: Decimal


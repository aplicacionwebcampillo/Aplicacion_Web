from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoResponse
from app.crud import pedido as crud
from app.database import get_db

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post("/", response_model=PedidoResponse)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return serialize_pedido(crud.create_pedido(db, pedido))

@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(db)
    return [serialize_pedido(p) for p in pedidos]

@router.get("/{id_pedido}", response_model=PedidoResponse)
def obtener_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = crud.get_pedido(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return serialize_pedido(pedido)

@router.put("/{id_pedido}", response_model=PedidoResponse)
def actualizar_pedido(id_pedido: int, pedido_update: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = crud.update_pedido(db, id_pedido, pedido_update)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return serialize_pedido(pedido)

@router.delete("/{id_pedido}", response_model=PedidoResponse)
def eliminar_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = crud.delete_pedido(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return serialize_pedido(pedido)

def serialize_pedido(pedido):
    return {
        "id_pedido": pedido.id_pedido,
        "descuento": pedido.descuento,
        "precio_total": pedido.precio_total,
        "productos": [{
            "id_producto": pp.producto.id_producto,
            "nombre": pp.producto.nombre,
            "descripcion": pp.producto.descripcion,
            "precio": float(pp.producto.precio),
            "stock": pp.producto.stock,
            "imagen": pp.producto.imagen,
            "cantidad": pp.cantidad
        } for pp in pedido.pedido_productos]
    }


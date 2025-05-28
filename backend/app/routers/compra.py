from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.compra import CompraCreate, CompraResponse, CompraUpdate
from app.crud import compra as crud
from app.database import get_db
from app.models import Usuario
from app.models import Pedido
from app.models import pedido_producto
from app.models import Producto
from app.utils.emails_utils import enviar_correos

import asyncio

router = APIRouter(prefix="/compras", tags=["compras"])


@router.post("/", response_model=CompraResponse)
async def registrar_compra(compra: CompraCreate, db: Session = Depends(get_db)):
    # Crear la compra (sin pasar productos)
    compra_creada = crud.create_compra(db, compra)

    # Obtener el usuario desde la base de datos
    usuario = db.query(Usuario).filter(Usuario.dni == compra_creada.dni).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cliente_email = usuario.email

    # Obtener el pedido para el total
    pedido = db.query(Pedido).filter(Pedido.id_pedido == compra_creada.id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Preparar detalles de productos (usando lo recibido, no desde DB relacional)
    detalle_lineas = []
    for p in compra.productos:
        producto = db.query(Producto).filter(Producto.id_producto == p.id_producto).first()
        if producto:
            detalle_lineas.append(
                f"- {producto.nombre} (ID: {producto.id_producto})\n"
                f"  Cantidad: {p.cantidad}, Talla: {p.talla}"
            )
        else:
            detalle_lineas.append(
                f"- Producto desconocido (ID: {p.id_producto})\n"
                f"  Cantidad: {p.cantidad}, Talla: {p.talla}"
            )

    detalle_productos = "\n".join(detalle_lineas)

    # Enviar correos
    await enviar_correos(
        cliente_email=cliente_email,
        asunto_cliente="Compra registrada correctamente",
        cuerpo_cliente=(
            f"Hola {usuario.nombre},\n\n"
            f"Gracias por tu compra. Detalles:\n\n"
            f"ID Compra: {compra_creada.id_pedido}\n"
            f"Fecha: {compra_creada.fecha_compra}\n"
            f"Productos:\n{detalle_productos}\n\n"
            f"Total: {pedido.precio_total} €\n"
        ),
        asunto_admin="Nueva compra registrada",
        cuerpo_admin=(
            f"Se ha registrado una nueva compra:\n\n"
            f"Usuario: {usuario.nombre} ({usuario.email})\n"
            f"DNI: {usuario.dni}\n"
            f"ID Compra: {compra_creada.id_pedido}\n"
            f"Fecha: {compra_creada.fecha_compra}\n"
            f"Productos:\n{detalle_productos}\n\n"
            f"Total: {pedido.precio_total} €\n"
        )
    )

    return compra_creada



@router.get("/", response_model=List[CompraResponse])
def listar_compras(db: Session = Depends(get_db)):
    return crud.get_compras(db)
    
@router.put("/validar_pago/{dni}")
def validar_pago_compra(dni: str, db: Session = Depends(get_db)):
    return crud.validar_pago_compra(db, dni)

@router.get("/{dni}/{id_pedido}", response_model=CompraResponse)
def obtener_compra(dni: str, id_pedido: int, db: Session = Depends(get_db)):
    compra = crud.get_compra(db, dni, id_pedido)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra

@router.put("/{dni}/{id_pedido}", response_model=CompraResponse)
def actualizar_compra(dni: str, id_pedido: int, compra_update: CompraUpdate, db: Session = Depends(get_db)):
    compra = crud.update_compra(db, dni, id_pedido, compra_update)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra

@router.delete("/{dni}/{id_pedido}")
def eliminar_compra(dni: str, id_pedido: int, db: Session = Depends(get_db)):
    ok = crud.delete_compra(db, dni, id_pedido)
    if not ok:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return {"ok": True, "mensaje": "Compra eliminada correctamente"}


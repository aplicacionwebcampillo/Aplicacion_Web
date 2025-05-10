from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.carrito import AgregarProducto, AplicarDescuento
from app.crud import carrito as crud
from app.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.get("/")
def obtener_carrito(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return crud.obtener_carrito(db, current_user.dni)

@router.post("/agregar")
def agregar_producto(
    datos: AgregarProducto,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    crud.agregar_producto(db, current_user.dni, datos)
    return {"mensaje": "Producto agregado al carrito"}

@router.put("/actualizar")
def actualizar_cantidad(
    id_producto: int,
    cantidad: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    crud.actualizar_cantidad(db, current_user.dni, id_producto, cantidad)
    return {"mensaje": "Cantidad actualizada"}

@router.post("/descuento")
def aplicar_descuento(
    datos: AplicarDescuento,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    crud.aplicar_descuento(db, current_user.dni, datos)
    return {"mensaje": "Descuento aplicado"}

@router.post("/confirmar")
def confirmar_pedido(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedido_id = crud.confirmar_pedido(db, current_user.dni)
    if pedido_id is None:
        raise HTTPException(status_code=400, detail="Carrito vacío")
    return {"mensaje": "Pedido confirmado", "id_pedido": pedido_id}


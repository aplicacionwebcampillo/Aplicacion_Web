from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioBase
from app.dependencies import get_db, get_current_user
from app.crud import carrito as carrito_crud
from app.core.auth import get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from app.schemas.carrito import CarritoResponse
from app.models.producto import Producto
from app.schemas.producto import ProductoSchema
from typing import List

router = APIRouter(prefix="/carrito", tags=["Carrito"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get("/", response_model=List[ProductoSchema])
def obtener_carrito(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()  # Consulta SQLAlchemy para obtener los productos
    return [ProductoSchema.from_orm(producto) for producto in productos]  # Convierte a Pydantic


@router.post("/agregar", summary="Agregar producto al carrito")
def agregar_producto(
    producto_id: int,
    cantidad: int = 1,
    db: Session = Depends(get_db),
    current_user: UsuarioBase = Depends(get_current_user)
):
    return carrito_crud.agregar_producto(db, current_user.dni, producto_id, cantidad)


@router.put("/actualizar", summary="Actualizar cantidad de un producto")
def actualizar_producto(
    producto_id: int,
    cantidad: int,
    current_user: UsuarioBase = Depends(get_current_user)
):
    return carrito_crud.actualizar_producto(current_user.dni, producto_id, cantidad)


@router.post("/descuento", summary="Aplicar código de descuento")
def aplicar_descuento(
    codigo: str,
    db: Session = Depends(get_db),
    current_user: UsuarioBase = Depends(get_current_user)
):
    return carrito_crud.aplicar_descuento(db, current_user.dni, codigo.upper())


@router.post("/confirmar", summary="Confirmar el pedido")
def confirmar_pedido(
    db: Session = Depends(get_db),
    current_user: UsuarioBase = Depends(get_current_user)
):
    return carrito_crud.confirmar_pedido(db, current_user.dni)


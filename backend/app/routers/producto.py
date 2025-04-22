from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.database import get_db
from app.crud import producto as crud

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_producto(db, producto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip, limit)

@router.get("/{nombre}", response_model=ProductoResponse)
def obtener_producto(nombre: str, db: Session = Depends(get_db)):
    producto = crud.get_producto(db, nombre)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{nombre}", response_model=ProductoResponse)
def actualizar_producto(nombre: str, producto_update: ProductoUpdate, db: Session = Depends(get_db)):
    producto = crud.update_producto(db, nombre, producto_update)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{nombre}")
def eliminar_producto(nombre: str, db: Session = Depends(get_db)):
    ok = crud.delete_producto(db, nombre)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True, "mensaje": "Producto eliminado correctamente"}


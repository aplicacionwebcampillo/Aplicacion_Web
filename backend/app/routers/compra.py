from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.compra import CompraCreate, CompraResponse, CompraUpdate
from app.crud import compra as crud
from app.database import get_db

router = APIRouter(prefix="/compras", tags=["compras"])

@router.post("/", response_model=CompraResponse)
def registrar_compra(compra: CompraCreate, db: Session = Depends(get_db)):
    return crud.create_compra(db, compra)

@router.get("/", response_model=List[CompraResponse])
def listar_compras(db: Session = Depends(get_db)):
    return crud.get_compras(db)

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


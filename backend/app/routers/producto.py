from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.producto import ProductoCreate
from app.crud import producto as crud
from app.database import get_db

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)


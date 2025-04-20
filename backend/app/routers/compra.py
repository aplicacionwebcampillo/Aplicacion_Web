from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.compra import CompraCreate
from app.crud import compra as crud
from app.database import get_db

router = APIRouter(prefix="/compras", tags=["compras"])

@router.post("/")
def registrar_compra(compra: CompraCreate, db: Session = Depends(get_db)):
    return crud.create_compra(db, compra)


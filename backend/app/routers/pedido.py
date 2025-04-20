from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate
from app.crud import pedido as crud
from app.database import get_db

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post("/")
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return crud.create_pedido(db, pedido)


from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate

def create_producto(db: Session, producto: ProductoCreate):
    db.execute(text("SELECT agregar_producto(:nombre, :descripcion, :precio, :stock, :imagen)"), producto.dict())
    db.commit()

def delete_producto(db: Session, id_producto: int):
    db.execute(text("SELECT eliminar_producto(:id_producto)"), {"id_producto": id_producto})
    db.commit()


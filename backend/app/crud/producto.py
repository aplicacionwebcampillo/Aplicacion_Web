from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

def create_producto(db: Session, producto: ProductoCreate):
    db.execute(text("""
        CALL agregar_producto(
            :p_nombre, :p_descripcion, :p_precio, :p_stock, :p_imagen
        )
    """), {
        "p_nombre": producto.nombre,
        "p_descripcion": producto.descripcion,
        "p_precio": producto.precio,
        "p_stock": producto.stock,
        "p_imagen": producto.imagen
    })
    db.commit()
    return db.query(Producto).filter(Producto.nombre == producto.nombre).first()

def get_producto(db: Session, nombre: str):
    return db.query(Producto).filter(Producto.nombre == nombre).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()

def update_producto(db: Session, nombre: str, producto_update: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.nombre == nombre).first()
    if not producto:
        return None
    for key, value in producto_update.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    db.commit()
    db.refresh(producto)
    return producto

def delete_producto(db: Session, nombre: str):
    producto = db.query(Producto).filter(Producto.nombre == nombre).first()
    if producto:
        db.delete(producto)
    db.commit()
    return True


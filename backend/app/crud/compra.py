from sqlalchemy.orm import Session
from app.models.compra import Compra
from app.schemas.compra import CompraCreate, CompraUpdate
from fastapi import HTTPException
from app.models.usuario import Usuario

def create_compra(db: Session, compra: CompraCreate):
    db_compra = Compra(**compra.dict())
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def get_compra(db: Session, dni: str, id_pedido: int):
    return db.query(Compra).filter(Compra.dni == dni, Compra.id_pedido == id_pedido).first()

def get_compras(db: Session):
    return db.query(Compra).all()

def update_compra(db: Session, dni: str, id_pedido: int, compra_update: CompraUpdate):
    compra = get_compra(db, dni, id_pedido)
    if not compra:
        return None
    for key, value in compra_update.dict(exclude_unset=True).items():
        setattr(compra, key, value)
    db.commit()
    db.refresh(compra)
    return compra

def delete_compra(db: Session, dni: str, id_pedido: int):
    compra = get_compra(db, dni, id_pedido)
    if not compra:
        return False
    db.delete(compra)
    db.commit()
    return True

def validar_pago_compra(db: Session, dni: str):
    usuario = db.query(Usuario).filter(Usuario.dni == dni).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    compra = (
        db.query(Compra)
        .filter(Compra.dni == usuario.dni)
        .order_by(Compra.fecha_compra.desc())
        .first()
    )

    if not compra:
        raise HTTPException(status_code=404, detail="No se encontró compra para este usuario")

    compra.pagado = True
    db.commit()
    db.refresh(compra)
    return {"message": "Pago validado correctamente para la compra", "id": compra.id_pedido}



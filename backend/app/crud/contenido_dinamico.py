from sqlalchemy.orm import Session
from app.models.contenido_dinamico import ContenidoDinamico
from app.schemas.contenido_dinamico import ContenidoCreate, ContenidoUpdate
from typing import List, Optional


def crear_contenido(db: Session, contenido: ContenidoCreate):
    nuevo_contenido = ContenidoDinamico(**contenido.dict())
    db.add(nuevo_contenido)
    db.commit()
    db.refresh(nuevo_contenido)
    return nuevo_contenido


def get_contenidos(db: Session, skip: int = 0, limit: int = 100) -> List[ContenidoDinamico]:
    return db.query(ContenidoDinamico).offset(skip).limit(limit).all()


def obtener_contenido_por_lugar(db: Session, lugar: str) -> List[ContenidoDinamico]:
    return (
        db.query(ContenidoDinamico)
        .filter(ContenidoDinamico.lugar == lugar)
        .order_by(ContenidoDinamico.orden.asc())
        .all()
    )


def get_contenido(db: Session, contenido_id: int):
    return db.query(ContenidoDinamico).filter(ContenidoDinamico.id == contenido_id).first()


def actualizar_contenido(db: Session, contenido_id: int, datos_actualizados: ContenidoUpdate):
    contenido = get_contenido(db, contenido_id)
    if not contenido:
        return None

    for campo, valor in datos_actualizados.dict(exclude_unset=True).items():
        setattr(contenido, campo, valor)

    db.commit()
    db.refresh(contenido)
    return contenido


def eliminar_contenido(db: Session, contenido_id: int):
    contenido = get_contenido(db, contenido_id)
    if not contenido:
        return False

    db.delete(contenido)
    db.commit()
    return True



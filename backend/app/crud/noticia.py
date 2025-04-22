from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.noticia import Noticia
from app.schemas.noticia import NoticiaCreate, NoticiaUpdate

def create_noticia(db: Session, noticia: NoticiaCreate):
    db.execute(text("""
        SELECT publicar_noticia(
            :p_titular, :p_imagen, :p_contenido, :p_categoria, :p_dni_administrador
        )
    """), {
        "p_titular": noticia.titular,
        "p_imagen": noticia.imagen,
        "p_contenido": noticia.contenido,
        "p_categoria": noticia.categoria,
        "p_dni_administrador": noticia.dni_administrador
    })
    db.commit()
    return db.query(Noticia).filter(Noticia.titular == noticia.titular).first()

def get_noticia(db: Session, titular: str):
    return db.query(Noticia).filter(Noticia.titular == titular).first()

def get_noticias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Noticia).offset(skip).limit(limit).all()

def update_noticia(db: Session, titular: str, noticia_update: NoticiaUpdate):
    noticia = db.query(Noticia).filter(Noticia.titular == titular).first()
    if not noticia:
        return None
    for key, value in noticia_update.dict(exclude_unset=True).items():
        setattr(noticia, key, value)
    db.commit()
    db.refresh(noticia)
    return noticia

def delete_noticia(db: Session, titular: str):
    noticia = db.query(Noticia).filter(Noticia.titular == titular).first()
    if noticia:
        db.delete(noticia)
    db.commit()
    return True


from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.noticia import Noticia
from app.schemas.noticia import NoticiaCreate

def create_noticia(db: Session, noticia: NoticiaCreate):
    db.execute(text("SELECT publicar_noticia(:titular, :imagen, :contenido, :categoria)"), noticia.dict())
    db.commit()

def delete_noticia(db: Session, id_noticia: int):
    db.execute(text("SELECT eliminar_noticia(:id_noticia)"), {"id_noticia": id_noticia})
    db.commit()


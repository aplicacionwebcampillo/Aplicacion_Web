from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.post_foro import PostForo
from app.schemas.foro import PostForoCreate

def create_post_foro(db: Session, post: PostForoCreate):
    db.execute(text("SELECT crear_post_foro(:contenido, :tipo, :dni_socio)"), post.dict())
    db.commit()

def delete_post_foro(db: Session, id_post: int):
    db.execute(text("SELECT eliminar_post_foro(:id_post)"), {"id_post": id_post})
    db.commit()


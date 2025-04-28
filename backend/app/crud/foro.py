from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.post_foro import PostForo
from app.schemas.foro import PostForoCreate, PostForoUpdate
from fastapi import HTTPException


def create_post_foro(db: Session, post_foro: PostForoCreate):
    db.execute(text("""
        SELECT crear_post_foro(
            :p_contenido, :p_tipo, :p_dni_usuario
        )
    """), {
        "p_contenido": post_foro.contenido,
        "p_tipo": post_foro.tipo,
        "p_dni_usuario": post_foro.dni_usuario
    })
    db.commit()
    return db.query(PostForo).filter(PostForo.contenido == post_foro.contenido).first()

def get_post_foro(db: Session, id_post: str):
    return db.query(PostForo).filter(PostForo.id_post == id_post).first()

def get_posts_foro(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PostForo).offset(skip).limit(limit).all()

def update_post_foro(db: Session, id_post: str, post_foro_update: PostForoUpdate):
    post_foro = db.query(PostForo).filter(PostForo.id_post == id_post).first()
    if not post_foro:
        return None
    for key, value in post_foro_update.dict(exclude_unset=True).items():
        setattr(post_foro, key, value)
    db.commit()
    db.refresh(post_foro)
    return post_foro

def delete_post_foro(db: Session, dni: str, id_post: int):
    try:
        db.execute(text("""
            SELECT eliminar_post_foro(
                :p_id_post, :p_dni
            )
        """), {
            "p_id_post": id_post,
            "p_dni": dni
        })
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))




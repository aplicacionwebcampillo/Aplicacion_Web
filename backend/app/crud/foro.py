from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.post_foro import PostForo
from app.schemas.foro import PostForoCreate, PostForoUpdate

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

def get_post_foro(db: Session, contenido: str):
    return db.query(PostForo).filter(PostForo.contenido == contenido).first()

def get_posts_foro(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PostForo).offset(skip).limit(limit).all()

def update_post_foro(db: Session, contenido: str, post_foro_update: PostForoUpdate):
    post_foro = db.query(PostForo).filter(PostForo.contenido == contenido).first()
    if not post_foro:
        return None
    for key, value in post_foro_update.dict(exclude_unset=True).items():
        setattr(post_foro, key, value)
    db.commit()
    db.refresh(post_foro)
    return post_foro

def delete_post_foro(db: Session, contenido: str):
    post_foro = db.query(PostForo).filter(PostForo.contenido == contenido).first()
    if post_foro:
        db.delete(post_foro)
    db.commit()
    return True



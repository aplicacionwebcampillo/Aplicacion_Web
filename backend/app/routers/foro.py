
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.foro import PostForoCreate, PostForoUpdate, PostForoResponse
from app.database import get_db
from app.crud import foro as crud

router = APIRouter(prefix="/posts_foro", tags=["Posts_foro"])

@router.post("/", response_model=PostForoResponse)
def crear_post_foro(post_foro: PostForoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_post_foro(db, post_foro)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PostForoResponse])
def listar_posts_foro(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts_foro(db, skip, limit)

@router.get("/{id_post}", response_model=PostForoResponse)
def obtener_post_foro(id_post: str, db: Session = Depends(get_db)):
    post_foro = crud.get_post_foro(db, id_post)
    if not post_foro:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post_foro

@router.put("/{id_post}", response_model=PostForoResponse)
def actualizar_post_foro(id_post: str, post_foro_update: PostForoUpdate, db: Session = Depends(get_db)):
    post_foro = crud.update_post_foro(db, id_post, post_foro_update)
    if not post_foro:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post_foro

@router.delete("{id_post}")
def eliminar_post_foro(id_post: int, dni: str, db: Session = Depends(get_db)):
    return crud.delete_post_foro(db, dni, id_post)
    if not ok:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return {"ok": True, "mensaje": "Post eliminado correctamente"}


@router.put("/moderar/{id_post}")
def moderar_post(id_post: int, db: Session = Depends(get_db)):
    return crud.moderar_post(db, id_post)


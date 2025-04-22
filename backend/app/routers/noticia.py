from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.noticia import NoticiaCreate, NoticiaUpdate, NoticiaResponse
from app.database import get_db
from app.crud import noticia as crud

router = APIRouter(prefix="/noticias", tags=["Noticias"])

@router.post("/", response_model=NoticiaResponse)
def crear_noticia(noticia: NoticiaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_noticia(db, noticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[NoticiaResponse])
def listar_noticias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_noticias(db, skip, limit)

@router.get("/{titular}", response_model=NoticiaResponse)
def obtener_noticia(titular: str, db: Session = Depends(get_db)):
    noticia = crud.get_noticia(db, titular)
    if not noticia:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return noticia

@router.put("/{titular}", response_model=NoticiaResponse)
def actualizar_noticia(titular: str, noticia_update: NoticiaUpdate, db: Session = Depends(get_db)):
    noticia = crud.update_noticia(db, titular, noticia_update)
    if not noticia:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return noticia

@router.delete("/{titular}")
def eliminar_noticia(titular: str, db: Session = Depends(get_db)):
    ok = crud.delete_noticia(db, titular)
    if not ok:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return {"ok": True, "mensaje": "Noticia eliminada correctamente"}


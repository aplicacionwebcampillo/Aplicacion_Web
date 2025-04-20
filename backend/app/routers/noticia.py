from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.noticia import NoticiaCreate
from app.crud import noticia as crud
from app.database import get_db

router = APIRouter(prefix="/noticias", tags=["noticias"])

@router.post("/")
def publicar_noticia(noticia: NoticiaCreate, db: Session = Depends(get_db)):
    return crud.create_noticia(db, noticia)


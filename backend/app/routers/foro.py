from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.foro import PostForoCreate
from app.crud import foro as crud
from app.database import get_db

router = APIRouter(prefix="/foro", tags=["foro"])

@router.post("/")
def crear_post_foro(post: PostForoCreate, db: Session = Depends(get_db)):
    return crud.create_post_foro(db, post)


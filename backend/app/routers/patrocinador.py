from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.patrocinador import PatrocinadorCreate
from app.crud import patrocinador as crud
from app.database import get_db

router = APIRouter(prefix="/patrocinadores", tags=["patrocinadores"])

@router.post("/")
def agregar_patrocinador(patrocinador: PatrocinadorCreate, db: Session = Depends(get_db)):
    return crud.create_patrocinador(db, patrocinador)


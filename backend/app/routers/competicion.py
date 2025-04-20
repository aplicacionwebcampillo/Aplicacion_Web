from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.competicion import CompeticionCreate
from app.crud import competicion as crud
from app.database import get_db

router = APIRouter(prefix="/competiciones", tags=["competiciones"])

@router.post("/")
def agregar_competicion(competicion: CompeticionCreate, db: Session = Depends(get_db)):
    return crud.create_competicion(db, competicion)


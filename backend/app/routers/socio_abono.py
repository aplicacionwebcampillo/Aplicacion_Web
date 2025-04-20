from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.socio_abono import SocioAbonoCreate
from app.crud import socio_abono as crud
from app.database import get_db

router = APIRouter(prefix="/socio-abono", tags=["socio_abono"])

@router.post("/")
def asociar_abono_socio(data: SocioAbonoCreate, db: Session = Depends(get_db)):
    return crud.create_socio_abono(db, data)

@router.get("/socio/{dni}")
def ver_abonos(dni: str, db: Session = Depends(get_db)):
    return crud.get_abonos_por_socio(db, dni)


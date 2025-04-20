from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.administrador import AdministradorCreate, AdministradorUpdate, AdministradorResponse
from app.database import get_db
from app.crud import administrador as crud

router = APIRouter(prefix="/administradores", tags=["Administradores"])

@router.post("/", response_model=AdministradorResponse)
def crear_administrador(admin: AdministradorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_administrador(db, admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AdministradorResponse])
def listar_administradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_administradores(db, skip, limit)

@router.get("/{dni}", response_model=AdministradorResponse)
def obtener_administrador(dni: str, db: Session = Depends(get_db)):
    admin = crud.get_administrador(db, dni)
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return admin

@router.put("/{dni}", response_model=AdministradorResponse)
def actualizar_administrador(dni: str, admin_update: AdministradorUpdate, db: Session = Depends(get_db)):
    admin = crud.update_administrador(db, dni, admin_update)
    if not admin:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return admin

@router.delete("/{dni}")
def eliminar_administrador(dni: str, db: Session = Depends(get_db)):
    ok = crud.delete_administrador(db, dni)
    if not ok:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return {"ok": True, "mensaje": "Administrador eliminado correctamente"}


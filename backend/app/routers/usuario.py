from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.crud import usuario as crud_usuario
from app.database import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, usuario.dni)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    return crud_usuario.create_usuario(db, usuario)

@router.get("/{dni}", response_model=UsuarioResponse)
def obtener_usuario(dni: str, db: Session = Depends(get_db)):
    usuario = crud_usuario.get_usuario(db, dni)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{dni}", response_model=UsuarioResponse)
def actualizar_usuario(dni: str, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.update_usuario(db, dni, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{dni}", response_model=UsuarioResponse)
def eliminar_usuario(dni: str, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.delete_usuario(db, dni)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


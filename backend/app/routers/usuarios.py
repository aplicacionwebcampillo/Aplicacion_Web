from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.crud.usuario import crear_usuario
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios/", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)

@router.get("/usuarios/")
def listar_usuarios():
    return [{"nombre": "Gabriel"}]

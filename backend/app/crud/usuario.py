from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.auth import get_password_hash

def get_usuario(db: Session, dni: str):
    return db.query(Usuario).filter(Usuario.dni == dni).first()

def get_usuarios(db: Session):
    return db.query(Usuario).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.contrasena)
    db_usuario = Usuario(**usuario.dict(exclude={"contrasena"}), contrasena=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, dni: str, usuario: UsuarioUpdate):
    db_usuario = get_usuario(db, dni)
    if not db_usuario:
        return None
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, dni: str):
    db_usuario = get_usuario(db, dni)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario


from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

def get_usuario(db: Session, dni: str):
    return db.query(Usuario).filter(Usuario.dni == dni).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
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


from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.models.usuario import Usuario
from app.models.administrador import Administrador
from app.schemas.administrador import AdministradorCreate, AdministradorUpdate

def create_administrador(db: Session, admin: AdministradorCreate):
    db.execute(text("""
        SELECT registrar_administrador(
            :p_dni, :p_nombre, :p_apellidos, :p_telefono,
            :p_fecha_nacimiento, :p_email, :p_contrasena,
            :p_cargo, :p_permisos
        )
    """), {
        "p_dni": admin.dni,
        "p_nombre": admin.nombre,
        "p_apellidos": admin.apellidos,
        "p_telefono": admin.telefono,
        "p_fecha_nacimiento": admin.fecha_nacimiento,
        "p_email": admin.email,
        "p_contrasena": admin.contrasena,
        "p_cargo": admin.cargo,
        "p_permisos": admin.permisos
    })
    db.commit()
    return db.query(Administrador).filter(Administrador.dni == admin.dni).first()

def get_administrador(db: Session, dni: str):
    return db.query(Administrador).filter(Administrador.dni == dni).first()

def get_administradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Administrador).offset(skip).limit(limit).all()

def update_administrador(db: Session, dni: str, admin_update: AdministradorUpdate):
    admin = db.query(Administrador).filter(Administrador.dni == dni).first()
    if not admin:
        return None
    for key, value in admin_update.dict(exclude_unset=True).items():
        setattr(admin, key, value)
    db.commit()
    db.refresh(admin)
    return admin

def delete_administrador(db: Session, dni: str):
    admin = db.query(Administrador).filter(Administrador.dni == dni).first()
    usuario = db.query(Usuario).filter(Usuario.dni == dni).first()
    if admin:
        db.delete(admin)
    if usuario:
        db.delete(usuario)
    db.commit()
    return True


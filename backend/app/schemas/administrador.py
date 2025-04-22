from pydantic import BaseModel
from typing import Optional
from datetime import date

class AdministradorBase(BaseModel):
    dni: str
    cargo: str
    permisos: str
    estado: Optional[str] = "activo"
    foto_perfil: Optional[str] = ""

class AdministradorCreate(AdministradorBase):
    nombre: str
    apellidos: str
    telefono: Optional[str] = None
    fecha_nacimiento: date
    email: str
    contrasena: str

class AdministradorUpdate(BaseModel):
    cargo: Optional[str] = None
    permisos: Optional[str] = None
    estado: Optional[str] = None
    foto_perfil: Optional[str] = None

class AdministradorResponse(AdministradorBase):
    class Config:
        orm_mode = True


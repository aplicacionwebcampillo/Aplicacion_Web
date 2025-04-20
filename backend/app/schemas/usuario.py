from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Base para reutilizar
class UsuarioBase(BaseModel):
    dni: str
    nombre: str
    apellidos: str
    telefono: Optional[str]
    fecha_nacimiento: date
    email: EmailStr

# Crear
class UsuarioCreate(UsuarioBase):
    contrasena: str

# Actualizar
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None

# Respuesta
class UsuarioResponse(UsuarioBase):
    class Config:
        orm_mode = True


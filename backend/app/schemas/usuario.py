from pydantic import BaseModel, EmailStr
from datetime import date

class UsuarioBase(BaseModel):
    dni: str
    nombre: str
    apellidos: str
    telefono: str | None = None
    fecha_nacimiento: date
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioRead(UsuarioBase):
    pass


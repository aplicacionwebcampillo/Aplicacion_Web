from pydantic import BaseModel
from typing import Optional
from datetime import date

class SocioBase(BaseModel):
    dni: str
    num_socio: str
    tipo_membresia: str
    estado: Optional[str] = "activo"
    foto_perfil: Optional[str] = ""

class SocioCreate(SocioBase):
    nombre: str
    apellidos: str
    telefono: Optional[str] = None
    fecha_nacimiento: date
    email: str
    contrasena: str
    tipo_socio: str 
    num_socio: Optional[str] = None
    tipo_membresia: Optional[str] = None

class SocioUpdate(BaseModel):
    tipo_membresia: Optional[str] = None
    estado: Optional[str] = None
    foto_perfil: Optional[str] = None
    
class SocioResponse(SocioBase):
    class Config:
        orm_mode = True


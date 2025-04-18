from pydantic import BaseModel
from typing import Optional

class AdministradorBase(BaseModel):
    dni: str
    cargo: str
    permisos: str
    estado: Optional[str] = "activo"
    foto_perfil: Optional[str] = None

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorRead(AdministradorBase):
    pass


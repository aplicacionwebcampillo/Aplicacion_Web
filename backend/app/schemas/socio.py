from pydantic import BaseModel
from typing import Optional

class SocioBase(BaseModel):
    dni: str
    num_socio: str
    tipo_membresia: str
    estado: Optional[str] = "activo"
    foto_perfil: Optional[str] = None

class SocioCreate(SocioBase):
    pass

class SocioRead(SocioBase):
    pass


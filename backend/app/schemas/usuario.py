from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    tipo_usuario: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


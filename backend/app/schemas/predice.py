from pydantic import BaseModel

class PrediceBase(BaseModel):
    dni: str
    nombre_competicion: str
    temporada_competicion: str
    local: str
    visitante: str
    resultado: str
    pagado: bool = False

class PrediceCreate(PrediceBase):
    pass

class PrediceRead(PrediceBase):
    pass


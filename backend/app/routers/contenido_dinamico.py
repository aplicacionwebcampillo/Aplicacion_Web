from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import contenido_dinamico as crud_contenido
from app.schemas.contenido_dinamico import ContenidoCreate, ContenidoUpdate, ContenidoResponse
from app.database import get_db

router = APIRouter(prefix="/contenido", tags=["Contenido Dinámico"])


# Obtener todos los contenidos o por lugar
@router.get("/", response_model=List[ContenidoResponse])
def obtener_contenido(lugar: str = None, db: Session = Depends(get_db)):
    if lugar:
        return crud_contenido.obtener_contenido_por_lugar(db, lugar)
    return crud_contenido.obtener_contenido(db)

    
@router.get("/{contenido_id}", response_model=ContenidoResponse)
def obtener_contenido(contenido_id: int, db: Session = Depends(get_db)):
    contenido = crud_contenido.get_contenido(db, contenido_id)
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return contenido

@router.post("/", response_model=ContenidoResponse)
def crear_contenido(contenido: ContenidoCreate, db: Session = Depends(get_db)):
    db_contenido = crud_contenido.get_contenido(db, contenido.id)
    if db_contenido:
        raise HTTPException(status_code=400, detail="El contenido ya existe.")
    return crud_contenido.crear_contenido(db, contenido)

# Actualizar contenido
@router.put("/{contenido_id}", response_model=ContenidoResponse)
def actualizar_contenido(contenido_id: int, contenido_update:ContenidoUpdate, db: Session = Depends(get_db)):
    contenido = crud_contenido.actualizar_contenido(db, contenido_id, contenido_update)
    if contenido is None:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return contenido

# Eliminar contenido
@router.delete("/{contenido_id}", response_model=ContenidoResponse)
def eliminar_contenido(contenido_id: int, db: Session = Depends(get_db)):
    eliminado = crud_contenido.eliminar_contenido(db, contenido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return



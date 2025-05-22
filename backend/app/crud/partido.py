from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from app.models.partido import Partido
from app.schemas.partido import PartidoCreate, PartidoUpdate
from fastapi import HTTPException, status
from sqlalchemy import or_
from datetime import datetime
from app.models.equipo import Equipo


def create_partido(db: Session, partido: PartidoCreate) -> Partido:
    try:
        db_partido = Partido(
            nombre_competicion=partido.nombre_competicion,
            temporada_competicion=partido.temporada_competicion,
            local=partido.local,
            visitante=partido.visitante,
            dia=partido.dia,
            hora=partido.hora,
            jornada=partido.jornada,
            resultado_local=partido.resultado_local,
            resultado_visitante=partido.resultado_visitante,
            acta=partido.acta
        )
        db.add(db_partido)
        db.commit()
        db.refresh(db_partido)
        return db_partido
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un partido con los mismos equipos y competición"
        )


def get_partido(db: Session, nombre_competicion: str, temporada_competicion: str, local: str, visitante: str) -> Optional[Partido]:
    return db.query(Partido).filter_by(
        nombre_competicion=nombre_competicion,
        temporada_competicion=temporada_competicion,
        local=local,
        visitante=visitante
    ).first()


def get_partidos_completos(db: Session, nombre_competicion: Optional[str] = None, temporada_competicion: Optional[str] = None) -> List[Partido]:
    query = db.query(Partido)
    
    if nombre_competicion:
        query = query.filter_by(nombre_competicion=nombre_competicion)
    
    if temporada_competicion:
        query = query.filter_by(temporada_competicion=temporada_competicion)
    
    return query.all()


def update_partido(db: Session, nombre_competicion: str, temporada_competicion: str, local: str, visitante: str, partido: PartidoUpdate) -> Partido:
    db_partido = get_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    
    if db_partido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El partido no fue encontrado"
        )
    
    if partido.dia is not None:
        db_partido.dia = partido.dia
    if partido.hora is not None:
        db_partido.hora = partido.hora
    if partido.jornada is not None:
        db_partido.jornada = partido.jornada
    if partido.resultado_local is not None:
        db_partido.resultado_local = partido.resultado_local
    if partido.resultado_visitante is not None:
        db_partido.resultado_visitante = partido.resultado_visitante
    if partido.acta is not None:
        db_partido.acta = partido.acta

    db.commit()
    db.refresh(db_partido)
    
    return db_partido


def delete_partido(db: Session, nombre_competicion: str, temporada_competicion: str, local: str, visitante: str) -> None:
    db_partido = get_partido(db, nombre_competicion, temporada_competicion, local, visitante)
    
    if db_partido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El partido no fue encontrado"
        )
    
    db.delete(db_partido)
    db.commit()


def get_calendario_partidos(
    db: Session,
    nombre_competicion: str = None,
    temporada_competicion: str = None,
    categoria: str = None,
    jugado: bool = None,
):
    query = db.query(Partido)

    # Filtrado por competición
    if nombre_competicion and temporada_competicion:
        query = query.filter(
            Partido.nombre_competicion == nombre_competicion,
            Partido.temporada_competicion == temporada_competicion,
        )

    # Filtrado por categoría (equipo)
    if categoria:
        subquery = db.query(Equipo.categoria).filter(Equipo.categoria == categoria).subquery()
        query = query.filter(
            (Partido.local.in_(subquery)) | (Partido.visitante.in_(subquery))
        )

    # Filtrado por jugado
    if jugado is not None:
        now = datetime.now()
        if jugado:
            query = query.filter(
                (Partido.dia < now.date()) |
                ((Partido.dia == now.date()) & (Partido.hora <= now.time()))
            )
        else:
            query = query.filter(
                (Partido.dia > now.date()) |
                ((Partido.dia == now.date()) & (Partido.hora > now.time()))
            )

    # Orden final
    query = query.order_by(Partido.dia, Partido.hora)

    return query.all()


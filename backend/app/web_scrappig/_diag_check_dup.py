"""Diagnostico puntual: comprobar si hay filas duplicadas del partido
Arjonilla-Campillo con distinta clave (local/visitante con espacios o
comillas distintas), lo que explicaria que el PUT actualice una fila y la
comprobacion lea otra. Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.partido import Partido

session = SessionLocal()
try:
    partidos = (
        session.query(Partido)
        .filter(Partido.local.ilike("%arjonilla%"))
        .all()
    )
    print(f"Total filas con 'arjonilla' en local: {len(partidos)}", flush=True)
    for p in partidos:
        print(
            f"  nombre_competicion={p.nombre_competicion!r} temporada={p.temporada_competicion!r} "
            f"local={p.local!r} visitante={p.visitante!r} dia={p.dia} acta={p.acta!r}",
            flush=True,
        )
finally:
    session.close()

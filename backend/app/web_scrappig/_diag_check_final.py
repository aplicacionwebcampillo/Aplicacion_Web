"""Diagnostico puntual: comprobar el acta del partido de Cuartos tras la
ejecucion real del scraping con la nueva logica automatica. Se borra tras
usarlo."""
from app.database import SessionLocal
from app.models.partido import Partido

session = SessionLocal()
try:
    p = (
        session.query(Partido)
        .filter(Partido.local.ilike("%arjonilla%"), Partido.visitante.ilike("%campillo%"))
        .first()
    )
    if not p:
        print("No se encontro el partido.", flush=True)
    else:
        print(f"acta={p.acta!r}", flush=True)
finally:
    session.close()

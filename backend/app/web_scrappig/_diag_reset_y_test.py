"""Diagnostico puntual: vaciar el acta guardada a mano del partido de
Cuartos para comprobar, con una ejecucion real del scraper (main.py), si
la nueva logica de respaldo (buscar_acta_via_jornada) la encuentra sola de
verdad. Se borra tras usarlo."""
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
        print(f"ANTES acta={p.acta!r}", flush=True)
        p.acta = " "
        session.commit()
        print(f"DESPUES (vaciado) acta={p.acta!r}", flush=True)
finally:
    session.close()

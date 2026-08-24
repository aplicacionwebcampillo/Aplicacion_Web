"""Acción puntual: investigar por qué crear el partido de la final de Copa
falla con "Ya existe un partido con los mismos equipos y competición" pese a
que el GET del partido exacto devuelve 404. Partido tiene un
ForeignKeyConstraint hacia competicion(nombre, temporada), así que ese 400
también salta si NO existe la fila en `competicion` para esa competición y
temporada (el mensaje de error es genérico para cualquier IntegrityError).
Consulta directamente la BD (tablas competicion y partido) para confirmarlo.
Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.competicion import Competicion
from app.models.partido import Partido

NOMBRE = "Copa Andalucía 1ª Andaluza Sénior (Jaén)"
TEMPORADA = "Temporada 2025-2026"

session = SessionLocal()
try:
    print(f"[INFO] Filas en `competicion` con nombre={NOMBRE!r}:", flush=True)
    comps = session.query(Competicion).filter(Competicion.nombre == NOMBRE).all()
    for c in comps:
        print(f"    nombre={c.nombre!r} temporada={c.temporada!r}", flush=True)
    if not comps:
        print("    (ninguna)", flush=True)

    print(f"[INFO] ¿Existe competicion(nombre={NOMBRE!r}, temporada={TEMPORADA!r})?", flush=True)
    existe = session.query(Competicion).filter_by(nombre=NOMBRE, temporada=TEMPORADA).first()
    print(f"    {'SÍ' if existe else 'NO'}", flush=True)

    print(f"[INFO] Filas en `partido` con local o visitante relacionados con Canena/Campillo:", flush=True)
    partidos = (
        session.query(Partido)
        .filter(
            (Partido.local.ilike("%campillo%"))
            | (Partido.visitante.ilike("%campillo%"))
            | (Partido.local.ilike("%canena%"))
            | (Partido.visitante.ilike("%canena%"))
        )
        .all()
    )
    for p in partidos:
        print(
            f"    [{p.nombre_competicion!r} / {p.temporada_competicion!r}] "
            f"{p.local!r} vs {p.visitante!r} | dia={p.dia} hora={p.hora} jornada={p.jornada!r} "
            f"acta={p.acta!r}",
            flush=True,
        )
    if not partidos:
        print("    (ninguna)", flush=True)
finally:
    session.close()

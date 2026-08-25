"""Acción puntual: listar los jugadores con dorsal reservado para cuerpo
técnico (0, 26-30, ver DORSALES_CUERPO_TECNICO en JugadorDetalle.tsx) para
ver qué rol/posicion tiene cada uno ya en la BD. Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.jugador import Jugador

DORSALES_CUERPO_TECNICO = [0, 26, 27, 28, 29, 30]

session = SessionLocal()
try:
    jugadores = (
        session.query(Jugador)
        .filter(Jugador.dorsal.in_(DORSALES_CUERPO_TECNICO))
        .order_by(Jugador.dorsal)
        .all()
    )
    print(f"[INFO] {len(jugadores)} filas con dorsal de cuerpo técnico:", flush=True)
    for j in jugadores:
        print(
            f"  dorsal={j.dorsal} nombre={j.nombre!r} posicion={j.posicion!r} "
            f"id_equipo={j.id_equipo} biografia={ (j.biografia or '')[:80]!r}",
            flush=True,
        )
finally:
    session.close()

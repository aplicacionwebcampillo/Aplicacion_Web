"""Acción puntual: comprobar qué campos (foto, biografia) le faltan a cada
miembro del cuerpo técnico ya fichado, para saber a cuál le falló la
sincronización desde Instagram. Se borra tras usarlo."""
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
    for j in jugadores:
        print(
            f"dorsal={j.dorsal} nombre={j.nombre!r} posicion={j.posicion!r} "
            f"foto={j.foto!r} bio_len={len(j.biografia or '')}",
            flush=True,
        )
finally:
    session.close()

"""Diagnostico puntual: estado actual de jugadores senior (lapreferente)
tras la ultima ejecucion en local del usuario. Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.jugador import Jugador

session = SessionLocal()
try:
    jugadores = (
        session.query(Jugador)
        .filter(Jugador.id_equipo == 1)
        .order_by(Jugador.dorsal)
        .all()
    )
    for j in jugadores:
        print(
            f"  dorsal={j.dorsal:>2} nombre={j.nombre!r} posicion={j.posicion!r} "
            f"nombre_corto={j.nombre_corto!r} nombre_completo={j.nombre_completo!r} "
            f"estado_fichaje={j.estado_fichaje!r} PJ={j.partidos_jugados} PT={j.partidos_titular} "
            f"G={j.goles} TA={j.tarjetas_amarillas} TR={j.tarjetas_rojas}",
            flush=True,
        )
finally:
    session.close()

"""Diagnostico puntual: comprobar el estado actual de los datos de
lapreferente (nombre_corto, nombre_completo, estado_fichaje, estadisticas)
para la plantilla senior. Se borra tras usarlo."""
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
    print(f"Total jugadores senior: {len(jugadores)}", flush=True)
    sin_enriquecer = 0
    for j in jugadores:
        enriquecido = bool(j.nombre_corto or j.nombre_completo or j.estado_fichaje)
        if not enriquecido:
            sin_enriquecer += 1
        print(
            f"  dorsal={j.dorsal:>2} nombre={j.nombre!r} posicion={j.posicion!r} "
            f"nombre_corto={j.nombre_corto!r} nombre_completo={j.nombre_completo!r} "
            f"estado_fichaje={j.estado_fichaje!r} PJ={j.partidos_jugados} PT={j.partidos_titular} "
            f"G={j.goles} TA={j.tarjetas_amarillas} TR={j.tarjetas_rojas}",
            flush=True,
        )
    print(f"\nSin ningun dato de lapreferente (nombre_corto/nombre_completo/estado_fichaje vacios): {sin_enriquecer}", flush=True)
finally:
    session.close()

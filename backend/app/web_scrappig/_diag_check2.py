"""Diagnostico puntual: estado actual de jugadores senior (lapreferente) y
del ultimo partido jugado (acta). Se borra tras usarlo."""
from datetime import date

from app.database import SessionLocal
from app.models.jugador import Jugador
from app.models.partido import Partido

session = SessionLocal()
try:
    print("=" * 20 + " Jugadores senior " + "=" * 20, flush=True)
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

    print("\n" + "=" * 20 + " Ultimo partido REALMENTE jugado (dia <= hoy) " + "=" * 20, flush=True)
    hoy = date.today()
    print(f"  (hoy = {hoy})", flush=True)
    partidos = (
        session.query(Partido)
        .filter((Partido.local.ilike("%campillo%")) | (Partido.visitante.ilike("%campillo%")))
        .filter(Partido.dia <= hoy)
        .order_by(Partido.dia.desc())
        .limit(3)
        .all()
    )
    for p in partidos:
        print(
            f"  dia={p.dia} [{p.nombre_competicion!r}] {p.local!r} "
            f"{p.resultado_local}-{p.resultado_visitante} {p.visitante!r} "
            f"jornada={p.jornada!r} acta={p.acta!r}",
            flush=True,
        )
finally:
    session.close()

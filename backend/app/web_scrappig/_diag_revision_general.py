"""Acción puntual: revisar 3 cosas que reporta el usuario.
1) ¿Se guardó el acta del último partido jugado (ayer)?
2) ¿Qué hay en el dorsal 5 (jugadores "mezclados")?
3) Estado general de estadísticas de lapreferente en los jugadores.
Se borra tras usarlo."""
from datetime import date, timedelta

from app.database import SessionLocal
from app.models.partido import Partido
from app.models.jugador import Jugador
from app.models.resultado import Resultado

session = SessionLocal()
try:
    print("=" * 20 + " 1) ULTIMOS PARTIDOS (tabla partido) " + "=" * 20, flush=True)
    partidos = (
        session.query(Partido)
        .filter((Partido.local.ilike("%campillo%")) | (Partido.visitante.ilike("%campillo%")))
        .order_by(Partido.dia.desc())
        .limit(8)
        .all()
    )
    for p in partidos:
        print(
            f"  dia={p.dia} [{p.nombre_competicion!r}/{p.temporada_competicion!r}] "
            f"{p.local!r} {p.resultado_local}-{p.resultado_visitante} {p.visitante!r} "
            f"jornada={p.jornada!r} acta={p.acta!r}",
            flush=True,
        )

    print("\n" + "=" * 20 + " 1b) ULTIMOS RESULTADOS (tabla resultado) " + "=" * 20, flush=True)
    resultados = (
        session.query(Resultado)
        .filter((Resultado.local.ilike("%campillo%")) | (Resultado.visitante.ilike("%campillo%")))
        .order_by(Resultado.fecha.desc())
        .limit(8)
        .all()
    )
    for r in resultados:
        print(
            f"  fecha={r.fecha} {r.local!r} {r.goles_local}-{r.goles_visitante} {r.visitante!r} "
            f"jornada={r.jornada!r} categoria={r.categoria!r}",
            flush=True,
        )

    print("\n" + "=" * 20 + " 2) JUGADORES CON DORSAL 5 " + "=" * 20, flush=True)
    dorsal5 = session.query(Jugador).filter(Jugador.dorsal == 5).all()
    for j in dorsal5:
        print(
            f"  id={j.id_jugador} nombre={j.nombre!r} id_equipo={j.id_equipo} posicion={j.posicion!r} "
            f"nombre_corto={j.nombre_corto!r} nombre_completo={j.nombre_completo!r} "
            f"estado_fichaje={j.estado_fichaje!r} partidos_jugados={j.partidos_jugados} "
            f"titular={j.partidos_titular} goles={j.goles} amarillas={j.tarjetas_amarillas} "
            f"rojas={j.tarjetas_rojas} foto={'SI' if j.foto else 'NO'}",
            flush=True,
        )

    print("\n" + "=" * 20 + " 3) TODOS LOS JUGADORES SENIOR (equipo 1): resumen de estadisticas " + "=" * 20, flush=True)
    jugadores = session.query(Jugador).filter(Jugador.id_equipo == 1).order_by(Jugador.dorsal).all()
    for j in jugadores:
        print(
            f"  dorsal={j.dorsal} nombre={j.nombre!r} nombre_corto={j.nombre_corto!r} "
            f"estado_fichaje={j.estado_fichaje!r} PJ={j.partidos_jugados} PT={j.partidos_titular} "
            f"G={j.goles} TA={j.tarjetas_amarillas} TR={j.tarjetas_rojas}",
            flush=True,
        )
finally:
    session.close()

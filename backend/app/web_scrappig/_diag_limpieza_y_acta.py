"""Acción puntual:
1) Limpia nombre_corto/nombre_completo/estado_fichaje de los jugadores con
   dorsal 5 y 19, contaminados con los datos de otro jugador (Justin, dorsal
   14) por un fallo de emparejamiento en lapreferente_estadisticas_sync.py
   ya corregido. No se toca 'posicion' (campo obligatorio, no se puede
   vaciar sin saber el valor correcto).
2) Busca el último partido REALMENTE jugado (dia <= hoy) para ver si tiene
   acta.
Se borra tras usarlo."""
from datetime import date

from app.database import SessionLocal
from app.models.jugador import Jugador
from app.models.partido import Partido

session = SessionLocal()
try:
    print("=" * 20 + " Limpiando dorsales 5 y 19 " + "=" * 20, flush=True)
    for dorsal in (5, 19):
        j = session.query(Jugador).filter(Jugador.dorsal == dorsal, Jugador.id_equipo == 1).first()
        if not j:
            print(f"  dorsal={dorsal}: no encontrado", flush=True)
            continue
        print(
            f"  ANTES dorsal={dorsal} nombre={j.nombre!r} nombre_corto={j.nombre_corto!r} "
            f"nombre_completo={j.nombre_completo!r} estado_fichaje={j.estado_fichaje!r} posicion={j.posicion!r}",
            flush=True,
        )
        j.nombre_corto = None
        j.nombre_completo = None
        j.estado_fichaje = None
    session.commit()
    print("  [OK] Limpiado.", flush=True)

    print("\n" + "=" * 20 + " Ultimo partido REALMENTE jugado (dia <= hoy) " + "=" * 20, flush=True)
    hoy = date.today()
    print(f"  (hoy = {hoy})", flush=True)
    partidos = (
        session.query(Partido)
        .filter((Partido.local.ilike("%campillo%")) | (Partido.visitante.ilike("%campillo%")))
        .filter(Partido.dia <= hoy)
        .order_by(Partido.dia.desc())
        .limit(5)
        .all()
    )
    for p in partidos:
        print(
            f"  dia={p.dia} [{p.nombre_competicion!r}/{p.temporada_competicion!r}] "
            f"{p.local!r} {p.resultado_local}-{p.resultado_visitante} {p.visitante!r} "
            f"jornada={p.jornada!r} acta={p.acta!r}",
            flush=True,
        )
    if not partidos:
        print("  (ninguno encontrado con dia <= hoy)", flush=True)
finally:
    session.close()

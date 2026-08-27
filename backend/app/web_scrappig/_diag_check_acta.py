"""Diagnostico puntual:
1) Limpia nombre_corto/nombre_completo/estado_fichaje de los dorsales 13, 18
   y 19, que han vuelto a contaminarse (probablemente por una ejecucion en
   local de lapreferente_estadisticas_sync.py con una copia desactualizada,
   anterior al fix de emparejamiento). No se toca 'posicion'.
2) Comprueba si el ultimo partido REALMENTE jugado (dia <= hoy) ya tiene
   acta tras el ultimo scraping.
Se borra tras usarlo."""
from datetime import date

from app.database import SessionLocal
from app.models.jugador import Jugador
from app.models.partido import Partido

session = SessionLocal()
try:
    print("=" * 20 + " Limpiando dorsales 13, 18 y 19 " + "=" * 20, flush=True)
    for dorsal in (13, 18, 19):
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

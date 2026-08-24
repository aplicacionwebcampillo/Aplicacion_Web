"""Comprueba si el club jugó un partido AYER, consultando directamente la
tabla `resultados` (la que actualiza scraper_jornada.py, no requiere
Instagram ni lapreferente). Se usa en el workflow de recordatorio para
avisar el día siguiente a cada partido, en vez de un día fijo de la semana.

Requiere DATABASE_URL (igual que scraper_jornada.py) y PYTHONPATH=./backend.

Escribe "enviar=true"/"enviar=false" en $GITHUB_OUTPUT si existe (para que
el siguiente paso del workflow decida si manda el email), o simplemente lo
imprime si se ejecuta a mano fuera de GitHub Actions.
"""
import os
from datetime import date, timedelta

from app.database import SessionLocal
from app.models.resultado import Resultado

NOMBRE_EQUIPO = os.environ.get("NOMBRE_EQUIPO_RFAF", "campillo")


def main():
    ayer = (date.today() - timedelta(days=1)).isoformat()

    session = SessionLocal()
    try:
        partido = (
            session.query(Resultado)
            .filter(Resultado.fecha == ayer)
            .filter(
                (Resultado.local.ilike(f"%{NOMBRE_EQUIPO}%"))
                | (Resultado.visitante.ilike(f"%{NOMBRE_EQUIPO}%"))
            )
            .first()
        )
    finally:
        session.close()

    enviar = partido is not None
    if partido:
        print(
            f"[INFO] Partido de ayer encontrado: {partido.local} "
            f"{partido.goles_local}-{partido.goles_visitante} {partido.visitante} "
            f"({partido.categoria})",
            flush=True,
        )
    else:
        print(f"[INFO] No hay partido registrado para ayer ({ayer}): no se envía aviso.", flush=True)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"enviar={'true' if enviar else 'false'}\n")


if __name__ == "__main__":
    main()

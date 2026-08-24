"""Acción puntual: reproducir exactamente la consulta que hace
Calendario.tsx (las mismas 6 competiciones x 6 temporadas de Senior),
ordenar por fecha ascendente igual que el componente, y ver en qué posición
(página, con 9 por página) queda la final de Copa Canena-Campillo, para
entender por qué el usuario dice que no aparece ahí. Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.partido import Partido

COMPETICIONES = [
    "1ª Andaluza Sénior (Jaén)",
    "Fase Final 1ª Andaluza Sénior (Jaén)",
    "Copa Andalucía 1ª Andaluza Sénior (Jaén)",
    "Trofeo Copa Subdelegado del Gobierno (Jaén)",
    "Fase Final Trofeo Copa Subdelegado del Gobierno (Jaén)",
    "Trofeo Copa Presidente Diputación (Jaén)",
]
TEMPORADAS = [
    "Temporada 2024-2025",
    "Temporada 2025-2026",
    "Temporada 2026-2027",
    "Temporada 2027-2028",
    "Temporada 2028-2029",
    "Temporada 2029-2030",
]

session = SessionLocal()
try:
    partidos = (
        session.query(Partido)
        .filter(Partido.nombre_competicion.in_(COMPETICIONES))
        .filter(Partido.temporada_competicion.in_(TEMPORADAS))
        .all()
    )
    partidos.sort(key=lambda p: p.dia)

    print(f"[INFO] Total partidos (Senior, como Calendario.tsx): {len(partidos)}", flush=True)
    for i, p in enumerate(partidos):
        pagina = (i // 9) + 1
        marca = " <=== ESTE" if "CANENA" in p.local.upper() or "CANENA" in p.visitante.upper() else ""
        print(
            f"  [{i}] pagina={pagina} dia={p.dia} [{p.nombre_competicion!r}/{p.temporada_competicion!r}] "
            f"{p.local!r} vs {p.visitante!r} jornada={p.jornada!r}{marca}",
            flush=True,
        )
finally:
    session.close()

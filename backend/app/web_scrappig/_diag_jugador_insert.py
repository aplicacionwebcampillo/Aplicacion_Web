"""Diagnóstico temporal: por qué crear_jugador devuelve 500 para algunos
jugadores. Se conecta directamente a la BD (DATABASE_URL) e imprime los
dorsales ya usados en el equipo 1, y prueba a insertar (en una transacción
que se revierte siempre) los casos que fallaron en el workflow real, para
capturar el error real de Postgres en vez del "Internal Server Error"
genérico que devuelve la API."""

import os

from sqlalchemy import create_engine, text

engine = create_engine(os.environ["DATABASE_URL"])

with engine.connect() as conn:
    print("=== Jugadores actuales del equipo 1 (id_equipo, nombre, dorsal) ===", flush=True)
    for row in conn.execute(text("SELECT id_jugador, nombre, dorsal FROM jugador WHERE id_equipo = 1 ORDER BY dorsal")):
        print(dict(row._mapping), flush=True)

    print("\n=== Estructura de la tabla jugador (columnas) ===", flush=True)
    for row in conn.execute(text(
        "SELECT column_name, data_type, is_nullable FROM information_schema.columns "
        "WHERE table_name = 'jugador' ORDER BY ordinal_position"
    )):
        print(dict(row._mapping), flush=True)

    print("\n=== Restricciones (constraints) de la tabla jugador ===", flush=True)
    for row in conn.execute(text(
        "SELECT conname, contype, pg_get_constraintdef(oid) AS definicion "
        "FROM pg_constraint WHERE conrelid = 'jugador'::regclass"
    )):
        print(dict(row._mapping), flush=True)

    print("\n=== Índices de la tabla jugador ===", flush=True)
    for row in conn.execute(text(
        "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'jugador'"
    )):
        print(dict(row._mapping), flush=True)

casos = [
    ("Oscar Navarro", "Centrocampista", 5),
    ("Mohammed Slaoui", "Mediapunta / Extremo", 6),
    ("Alex Martínez", "Sin especificar", 10),
    ("Fran Muñoz", "Sin especificar", 9),
    ("Justin Emil Martínez", "Delantero", 14),
]

print("\n=== Probando cada inserción real (dentro de una transacción que se revierte) ===", flush=True)
for nombre, posicion, dorsal in casos:
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(
                text(
                    "INSERT INTO jugador (id_equipo, nombre, posicion, fecha_nacimiento, foto, biografia, dorsal) "
                    "VALUES (1, :nombre, :posicion, NULL, 'https://example.com/foto.jpg', NULL, :dorsal)"
                ),
                {"nombre": nombre, "posicion": posicion, "dorsal": dorsal},
            )
            print(f"[OK] Insertaría sin problema: {nombre} (dorsal {dorsal})", flush=True)
        except Exception as e:
            print(f"[ERROR] {nombre} (dorsal {dorsal}): {type(e).__name__}: {e}", flush=True)
        finally:
            trans.rollback()

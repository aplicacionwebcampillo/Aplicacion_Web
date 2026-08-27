"""Diagnostico puntual: replicar la logica de buscar_jugador() de
lapreferente_estadisticas_sync.py a mano, imprimiendo TODOS los candidatos
que entran por la via del subconjunto de palabras, para ver por que
'Martin'/'Martin Moreno Sanchez' no encuentra un candidato unico. Se borra
tras usarlo."""
import sys

sys.path.insert(0, "backend/app/web_scrappig")
from lapreferente_estadisticas_sync import _normalizar, _tokens, obtener_jugadores_existentes

jugadores = obtener_jugadores_existentes()
print(f"Total jugadores obtenidos de la API: {len(jugadores)}", flush=True)

nombre_corto, nombre_completo = "Martin", "Martin Moreno Sanchez"
exactos = {o for o in (_normalizar(nombre_completo), _normalizar(nombre_corto)) if o}
objetivos_tokens = [t for t in (_tokens(nombre_completo), _tokens(nombre_corto)) if t]

candidato_exacto = None
candidatos_por_palabra = []
for jugador in jugadores:
    textos = (jugador.get("nombre"), jugador.get("nombre_corto"), jugador.get("nombre_completo"))
    if any(_normalizar(t) in exactos for t in textos if t):
        print(f"[EXACTO] {jugador.get('nombre')!r} (dorsal={jugador.get('dorsal')}, id_equipo={jugador.get('id_equipo')})", flush=True)
        if candidato_exacto is None:
            candidato_exacto = jugador
        continue

    tokens_jugador = _tokens(jugador.get("nombre")) | _tokens(jugador.get("nombre_completo"))
    if not tokens_jugador:
        continue
    for obj_tokens in objetivos_tokens:
        compartidas = obj_tokens & tokens_jugador
        if not compartidas or max(len(p) for p in compartidas) < 4:
            continue
        if obj_tokens <= tokens_jugador or tokens_jugador <= obj_tokens:
            print(
                f"[CANDIDATO] {jugador.get('nombre')!r} (dorsal={jugador.get('dorsal')}, "
                f"id_equipo={jugador.get('id_equipo')}) tokens_jugador={tokens_jugador} obj_tokens={obj_tokens}",
                flush=True,
            )
            candidatos_por_palabra.append(jugador)
            break

print(f"\ncandidato_exacto={candidato_exacto}", flush=True)
print(f"len(candidatos_por_palabra)={len(candidatos_por_palabra)}", flush=True)

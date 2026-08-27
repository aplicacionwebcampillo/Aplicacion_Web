"""Diagnostico puntual: probar buscar_jugador() de
lapreferente_estadisticas_sync.py con el dato EXACTO de lapreferente para
Martin Moreno (visto en una captura real del usuario), contra la plantilla
actual real (vía API), para ver si el emparejamiento ya funciona o si sigue
fallando con el codigo actual. Se borra tras usarlo."""
import sys

sys.path.insert(0, "backend/app/web_scrappig")
from lapreferente_estadisticas_sync import buscar_jugador, obtener_jugadores_existentes

jugadores = obtener_jugadores_existentes()
print(f"Total jugadores obtenidos de la API: {len(jugadores)}", flush=True)

resultado = buscar_jugador("Martin", "Martin Moreno Sanchez", jugadores)
print(f"Resultado buscar_jugador('Martin', 'Martin Moreno Sanchez', ...): {resultado}", flush=True)

d5 = [j for j in jugadores if j.get("dorsal") == 5]
print(f"\nJugador dorsal=5 tal y como lo ve la API: {d5}", flush=True)

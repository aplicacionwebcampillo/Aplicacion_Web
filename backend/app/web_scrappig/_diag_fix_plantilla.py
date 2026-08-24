"""Acción puntual (no diagnóstico permanente): aplica de golpe la ronda de
correcciones de plantilla pedida por el club el 24/08/2026 -- jugadores con
dorsal reciclado sin dar de baja al anterior, un nombre con espacio de más
que rompía su ficha, y el resto del cuerpo técnico. Se borra tras usarlo."""
import requests

API_BASE = "https://aplicacion-web-m5oa.onrender.com"
ID_EQUIPO = 1


def eliminar(nombre):
    resp = requests.delete(f"{API_BASE}/jugadores/{nombre}", timeout=30)
    print(f"[{'OK' if resp.status_code == 200 else 'ERROR'}] DELETE '{nombre}' -> {resp.status_code} {resp.text[:200]}", flush=True)


def crear(nombre, posicion, dorsal, biografia=None):
    data = {
        "nombre": nombre,
        "posicion": posicion,
        "fecha_nacimiento": None,
        "foto": None,
        "biografia": biografia,
        "dorsal": dorsal,
        "id_equipo": ID_EQUIPO,
    }
    resp = requests.post(f"{API_BASE}/jugadores/", json=data, timeout=30)
    print(f"[{'OK' if resp.status_code in (200, 201) else 'ERROR'}] POST '{nombre}' (dorsal {dorsal}) -> {resp.status_code} {resp.text[:200]}", flush=True)


def actualizar(nombre_actual, datos):
    resp = requests.put(f"{API_BASE}/jugadores/{nombre_actual}", json=datos, timeout=30)
    print(f"[{'OK' if resp.status_code == 200 else 'ERROR'}] PUT '{nombre_actual}' {datos} -> {resp.status_code} {resp.text[:200]}", flush=True)


# 1) Arreglar el nombre con espacio de más (rompía /jugadores/:nombre)
actualizar("ROSENDO GALERA ", {"nombre": "ROSENDO GALERA"})

# 2) Dorsales con jugador antiguo sin dar de baja: borrar y crear el nuevo
eliminar("Oscar Navarro")
crear("Martín Moreno", "Defensa", 5)

eliminar("YERAY GONZALEZ JIMENEZ")
crear("Raúl Coronado", "Centrocampista", 6)

eliminar("JUAN MANUEL TRUJILLO BLE")  # sin reemplazo

eliminar("ALEJANDRO TIRADO BERRIO")
crear("Justin Emil Martínez", "Delantero", 14)

eliminar("ALFONSO PADILLA GARCIA")
crear("Antonio Carlos Navarro", "Lateral Derecho", 17)

eliminar("PABLO BATRES GONZALEZ")
crear("Álvaro Alarcón", "Centrocampista", 23)

# 3) Cristian Cortes cambia de rol (delegado de equipo), no se borra
actualizar("CHRISTIAN CORTES HERRANZ", {"dorsal": 30, "posicion": "Delegado de Equipo"})

# 4) Resto del cuerpo técnico, aún no existían
crear("Javi Salazar", "Segundo Entrenador", 27)
crear("Diego Merlo", "Preparador Físico", 28)
crear("Juanjo Mendoza", "Entrenador de Porteros", 29)

print("[FIN] Ronda de correcciones de plantilla completada.", flush=True)

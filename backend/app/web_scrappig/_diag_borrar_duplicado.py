"""Acción puntual: borra el partido "Descansa vs C.D. CAMPILLO DEL RÍO C.F.
'CD'" duplicado y obsoleto de Trofeo Copa Presidente Diputación (Jaén),
Temporada 2026-2027, jornada Cuartos -- ya se conoce el rival real (CLUB
ATLETICO ARJONILLA), que tiene su propio registro correcto. Se borra tras
usarlo."""
import asyncio

import httpx

URL_BASE = "https://aplicacion-web-m5oa.onrender.com"
NOMBRE = "Trofeo Copa Presidente Diputación (Jaén)"
TEMPORADA = "Temporada 2026-2027"
LOCAL = "Descansa"
VISITANTE = 'C.D. CAMPILLO DEL RÍO C.F. "CD"'


async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{URL_BASE}/partidos/{NOMBRE}/{TEMPORADA}/{LOCAL}/{VISITANTE}")
        print(f"[INFO] DELETE status={resp.status_code} body={resp.text!r}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())

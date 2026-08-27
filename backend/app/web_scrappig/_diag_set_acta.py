"""Diagnostico puntual: fijar a mano el acta del partido de Cuartos
(Arjonilla-Campillo, 26-08-2026), ya que la RFAF no la enlaza desde la
ficha de jornada de esta competicion (comprobado con y sin JavaScript).
URL confirmada por el usuario. Se borra tras usarlo."""
from app.database import SessionLocal
from app.models.partido import Partido

ACTA_URL = "https://www.rfaf.es/pnfg/NPcd/NFG_CmpPartido?cod_primaria=1000120&CodActa=2646248&cod_acta=2646248"

session = SessionLocal()
try:
    p = (
        session.query(Partido)
        .filter(Partido.local.ilike("%arjonilla%"), Partido.visitante.ilike("%campillo%"))
        .first()
    )
    if not p:
        print("No se encontro el partido.", flush=True)
    else:
        print(f"ANTES acta={p.acta!r}", flush=True)
        p.acta = ACTA_URL
        session.commit()
        print(f"DESPUES acta={p.acta!r}", flush=True)
finally:
    session.close()

from sqlalchemy.orm import Session
from sqlalchemy import text

def ceder_abono_temporal(db: Session, dni_cedente: str, dni_beneficiario: str, id_abono: int, fecha_inicio, fecha_fin):
    db.execute(text("SELECT ceder_abono_temporal(:dni_cedente, :dni_beneficiario, :id_abono, :fecha_inicio, :fecha_fin)"), {
        "dni_cedente": dni_cedente,
        "dni_beneficiario": dni_beneficiario,
        "id_abono": id_abono,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    })
    db.commit()


import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()  # carga las variables del .env

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

async def enviar_correos(cliente_email: str, asunto_cliente: str, cuerpo_cliente: str,
                        asunto_admin: str, cuerpo_admin: str):
    fm = FastMail(conf)

    msg_cliente = MessageSchema(
        subject=asunto_cliente,
        recipients=[cliente_email],
        body=cuerpo_cliente,
        subtype="plain"
    )

    msg_admin = MessageSchema(
        subject=asunto_admin,
        recipients=[ADMIN_EMAIL],
        body=cuerpo_admin,
        subtype="plain"
    )

    await fm.send_message(msg_cliente)
    await fm.send_message(msg_admin)


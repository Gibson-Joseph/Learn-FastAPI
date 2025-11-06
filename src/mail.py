from pathlib import Path
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

from .config import Config

# Path of the parent folder for this file, which in this case is src
BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    VALIDATE_CERTS=Config.VALIDATE_CERTS,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

mail = FastMail(config=mail_config)


def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message

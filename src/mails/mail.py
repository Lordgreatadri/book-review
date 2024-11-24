from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pathlib import Path
import smtplib
from src.config import Config


BASE_DIR = Path(__file__).resolve().parent


# Configure FastMail
configs = ConnectionConfig(
    MAIL_USERNAME=Config.mail_username,
    MAIL_PASSWORD=Config.mail_password,
    MAIL_FROM=Config.mail_from_email,
    MAIL_PORT=Config.mail_port,
    MAIL_SERVER=Config.mail_host,
    MAIL_FROM_NAME=Config.mail_from_name,
    MAIL_STARTTLS=Config.mail_starttls,
    MAIL_SSL_TLS=Config.mail_ssl_tls,
    USE_CREDENTIALS=Config.mail_use_credentials,
    VALIDATE_CERTS=Config.mail_validate_certs,
    # TEMPLATE_FOLDER=str(BASE_DIR, "templates/email"),

    # TEMPLATE_EXTENSION=".html"  # Default template extension is.html
)

# try:
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login("rexmerlo@gmail.com", "ivqm zwkc hzbc rpzc")
#     print("Connection successful!")
#     server.quit()
# except Exception as e:
#     print("Failed to connect:", e)


# Initialize FastMail
mail = FastMail(config=configs)
    


def create_message(recipients: list[str], subject: str, body: str):

    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )

    return message


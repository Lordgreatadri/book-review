
from asgiref.sync import async_to_sync
from celery import Celery
from src.mails.mail import mail, create_message

# set the environment variable to 'development' for using the local configuration
celery_app = Celery()
celery_app.config_from_object('src.config')

@celery_app.task()
def send_email(recipients:list[str], subject:str, body:str):
    message = create_message(recipients, subject, body)

    async_to_sync(mail.send_message)(message)  # Use the async version of the send_message method

    print(f"Sending email to {recipients}: {body}")

    return f"Email sent to {recipients}"


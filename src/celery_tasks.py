from celery import Celery
from asgiref.sync import async_to_sync

from src.mail import mail, create_message


c_app = Celery()

# 10:54:00
c_app.config_from_object("src.config")  # loads variables from config.py


@c_app.task()  # this is a Celery task
def send_email(recipents: list[str], subject: str, body: str):
    message = create_message(recipients=recipents, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("Email has been sent")

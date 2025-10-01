from src.infrastructure.celery.celery_app import celery_app
from src.services.mail.mail import mail_service


@celery_app.task
def send_confirmation_email_task(to_email: str, confirm_link: str):
    mail_service.send_confirmation_email(to_email, confirm_link)


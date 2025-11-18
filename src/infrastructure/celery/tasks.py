from src.infrastructure.celery.celery_app import celery_app
from src.infrastructure.notifications.email import EmailNotifications


@celery_app.task(name="email.send_email")
def send_confirmation_link_email(destination: str, subject: str, body: str):
    EmailNotifications().send_(destination, subject, body)

from src.infrastructure.celery.celery_app import celery_app
from src.infrastructure.notifications.email import EmailNotifications


@celery_app.task(name="email.send_confirmation_link_email")
def send_confirmation_link_email(destination: str, subject: str, body: str):
    EmailNotifications().send_(destination, subject, body)


@celery_app.task(name="email.send_respond_notification")
def send_respond_notification(destination: str, subject: str, body):
    EmailNotifications().send_(destination, subject, body)

import smtplib

from email.message import EmailMessage
from typing import Any

from loguru import logger

from src.core.config_reader import config
from src.interfaces.infrastructure.notifications import AbstractNotifications


class EmailNotifications(AbstractNotifications):
    def __init__(self):
        self.msg: EmailMessage | None = None

    def send(self, destination: str, template: str, data: dict[str, Any]) -> None:
        subject = data.get("subject")
        body = data.get("body")

        if template == "confirm_email":
            from src.infrastructure.celery.tasks import send_confirmation_link_email
            send_confirmation_link_email.delay(destination, subject, body)

        elif template == "send_respond_notification":
            from src.infrastructure.celery.tasks import send_respond_notification
            send_respond_notification.delay(destination, subject, body)

    def send_(self, destination: str, subject: str, body: str):
        self.msg = EmailMessage()
        self.msg["From"] = config.mail.smtp_user
        self.msg["Subject"] = subject
        self.msg["To"] = destination
        self.msg.set_content(body)

        logger.bind(
            app_name=f"{EmailNotifications.__name__} in {self.send.__name__}"
        ).info(f"DATA: TO_EMAIL {destination} | SUBJECT {subject} | BODY {body}")

        try:
            with smtplib.SMTP_SSL(config.mail.smtp_server, config.mail.smtp_port) as smtp:
                smtp.login(config.mail.smtp_user, config.mail.smtp_password)
                smtp.send_message(self.msg)

        except smtplib.SMTPException as exc:
            logger.bind(
                app_name=f"{EmailNotifications.__name__} in {self.send.__name__}"
            ).info(f"EXCEPTION {exc}")

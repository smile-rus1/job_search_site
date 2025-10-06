from loguru import logger

from src.infrastructure.mail.mailer import send_email


class EmailService:
    def send_confirmation_email(self, to_email: str, confirm_link: str):
        subject = "Подтвердите регистрацию на сайте"
        body = f"Перейдите по ссылке для подтверждения регистрации:\n{confirm_link}"

        logger.bind(
            app_name=f"{EmailService.__name__} in {self.send_confirmation_email.__name__}"
        ).info(f"DATA: TO_EMAIL {to_email} | SUBJECT {subject} | BODY {body}")

        send_email(to_email, subject, body)


def get_mail_service():
    return EmailService()


mail_service = get_mail_service()

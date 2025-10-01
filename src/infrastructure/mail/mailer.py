import smtplib

from email.message import EmailMessage

from src.core.config_reader import config


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = config.mail.smtp_user
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL(config.mail.smtp_server, config.mail.smtp_port) as smtp:
        smtp.login(config.mail.smtp_user, config.mail.smtp_password)
        smtp.send_message(msg)

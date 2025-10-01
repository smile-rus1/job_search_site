from dataclasses import dataclass


@dataclass
class MailConfig:
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    mail_from: str

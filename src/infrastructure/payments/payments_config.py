from dataclasses import dataclass


@dataclass
class StripePayment:
    publish_key: str
    secret_key: str
    webhook_secret: str


@dataclass
class PaymentsConfig:
    stripe_payment: StripePayment


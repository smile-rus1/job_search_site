import stripe

from src.core.config_reader import config
from src.infrastructure.payments.payments_config import StripePayment


def init_stripe(conf: StripePayment):
    stripe.api_key = conf.secret_key

    return stripe


stripe_instance = init_stripe(config.payments.stripe_payment)

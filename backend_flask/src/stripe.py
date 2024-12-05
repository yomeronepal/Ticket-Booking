import stripe
from stripe import (
    Customer,
    Account,
    Token,
    PaymentIntent,
    Payout,
    PaymentMethod,
    Charge,
    Refund,
)
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)
SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")


class StripeClient:
    def __init__(self) -> None:
        stripe.api_key = SECRET_KEY
        self.api_key = SECRET_KEY
        self.currency = "usd"
        pass


class StripeCheckout(StripeClient):
    def create_checkout_session(self, product_data):
        line_items = product_data
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"http://localhost:8000?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"http://localhost:8000",
            )
            return session
        except Exception as e:
            print(e)

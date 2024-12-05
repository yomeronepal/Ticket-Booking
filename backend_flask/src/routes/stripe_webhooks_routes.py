from flask import Blueprint, g
from ..controllers.stripe import stripe_webhooks
from ..middlewares.protect import protect

stripe_webhooks_routers = Blueprint("stripe", __name__)
stripe_webhooks_routers.add_url_rule(
    "",
    view_func=lambda: stripe_webhooks(),
    methods=["POST"],
    endpoint="stripe-webhooks",
)

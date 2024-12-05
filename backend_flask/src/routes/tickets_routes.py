from flask import Blueprint, g

from ..controllers.ticket import book_tickets, create_event, ticket_status
from ..middlewares.protect import protect
from ..middlewares.admin_protect import protect_admin

ticket_routes = Blueprint("ticket", __name__)
ticket_routes.add_url_rule(
    "/<int:event_id>",
    view_func=lambda event_id: protect(book_tickets)(event_id),
    methods=["POST"],
    endpoint="book-tickets",
)
ticket_routes.add_url_rule(
    "/event",
    view_func=lambda: protect(protect_admin(create_event))(),
    methods=["POST"],
    endpoint="create-event",
)

ticket_routes.add_url_rule(
    "/order/<int:id>",
    view_func=lambda id: protect(ticket_status)(id),
    methods=["GET"],
    endpoint="order-status",
)

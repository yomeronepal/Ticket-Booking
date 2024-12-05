from ..orm.user import UserORM
from ..database.tickets.models import Event, Ticket, Order
from flask import g


def validate_ticket_booking(data, event_id, user_id):
    if not data:
        raise ValueError("Data is required")
    event = Event.query.get(event_id)
    if "ticket_count" not in data:
        raise ValueError("Ticket count is required")
    ticket_count = data.get("ticket_count", None)
    if not event:
        raise ValueError("Event not found")

    sold_tickets = Ticket.query.filter(Ticket.status != "Available").count()
    available_tickets = event.total_tickets - sold_tickets
    if available_tickets < ticket_count:
        UserORM().create_wait_list(event_id, user_id, ticket_count)
        raise ValueError("Not enough tickets available")
    # Step 2: Lock Tickets in Redis
    lock_key = f"lock:{event_id}:{user_id}"
    if g.redis_client.exists(lock_key):
        raise ValueError("You already have tickets locked")
    return event

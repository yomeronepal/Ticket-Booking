from ..database.tickets.models import Event, Ticket, Order
from flask import g
from ..database import database as db


class BookingORM:
    def create_booking(self, user_id, event_id, checkout_session_id, ticket_count):
        print(checkout_session_id)
        event = Event.query.get(event_id)
        order = Order(
            user_id=user_id,
            event_id=event_id,
            status="Pending",
            stripe_session_id=checkout_session_id,
            total_price=ticket_count * event.price,
        )
        db.session.add(order)
        db.session.commit()
        tickets = [
            Ticket(event_id=event_id, status="Locked", order_id=order.id)
            for _ in range(ticket_count)
        ]
        db.session.bulk_save_objects(tickets)
        db.session.commit()
        return order

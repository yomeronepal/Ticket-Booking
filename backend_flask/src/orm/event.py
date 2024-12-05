from ..database.tickets.models import Event, Order
from ..database import database as db


class EventORM:
    def create_event(self, event_schema):
        event = Event(
            name=event_schema.name,
            date=event_schema.date,
            venue=event_schema.venue,
            price=event_schema.price,
            total_tickets=event_schema.total_tickets,
            sold_tickets=0,
            available_tickets=event_schema.total_tickets,
        )

        db.session.add(event)
        db.session.commit()
        return event


class OrderORM:
    def get_order(self, id):
        order = Order.query.get(id)
        return order

from ...database import database as db
from datetime import datetime
from sqlalchemy.orm import validates

# from ..models import User


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    venue = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    sold_tickets = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Event(name={self.name}, date={self.date}, venue={self.venue}, price={self.price}, total_tickets={self.total_tickets})>"


TICKET_STATUS_CHOICES = ("Available", "Locked", "Sold")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    stripe_session_id = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Float, nullable=True, default=0.00)

    # Relationships
    event = db.relationship("Event", backref=db.backref("orders", lazy=True))
    user = db.relationship("User", backref=db.backref("user_orders", lazy=True))

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, event_id={self.event_id}, status={self.status})>"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Available")
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)

    # Relationship
    event = db.relationship("Event", backref=db.backref("tickets", lazy=True))
    order = db.relationship("Order", backref=db.backref("order_tickets", lazy=True))

    def __repr__(self):
        return f"<Ticket(id={self.id}, event_id={self.event_id}, status={self.status})>"

    @validates("status")
    def validate_status(self, key, value):
        if value not in TICKET_STATUS_CHOICES:
            raise ValueError(
                f"Invalid status: {value}. Must be one of {TICKET_STATUS_CHOICES}."
            )
        return value


class TicketWaitList(db.Model):
    __tablename__ = "ticket_waitlist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    ticket_count = db.Column(db.Integer, nullable=False, default=1)

    # Relationships
    user = db.relationship(
        "User",
        backref=db.backref(
            "waitlisted_tickets", lazy="dynamic", cascade="all, delete-orphan"
        ),
    )
    event = db.relationship(
        "Event",
        backref=db.backref(
            "waitlisted_users", lazy="dynamic", cascade="all, delete-orphan"
        ),
    )

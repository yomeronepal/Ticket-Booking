from flask import request, jsonify, g
from datetime import datetime, timedelta

from ..orm.booking import BookingORM
from ..database.tickets.models import Event

# from ...src.database.orm.booking import BookingORM

from ..validator import validate_ticket_booking


from ..tasks.tasks import handle_ticket_availablity
from ..stripe import StripeCheckout
from ..utils.kafka import KafkaPublisher
from ..utils.email import Email
from ..pydantic.schemas import EventSchema, EventResponseSchema, OrderResposeSchema
from ..orm.event import EventORM, OrderORM


def book_tickets(event_id):
    # Send message to Kafka topic

    data = g.request_json_body
    user_id = g.user.id
    event = validate_ticket_booking(data, event_id, user_id)
    ticket_count = data.get("ticket_count")
    event = Event.query.get(event_id)
    product_data = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": event.name,
                },
                "unit_amount": int(event.price * 100),  # Convert to cents
            },
            "quantity": ticket_count,
        }
    ]
    stripe_checkout = StripeCheckout()
    checkout_session = stripe_checkout.create_checkout_session(product_data)
    order = BookingORM().create_booking(
        user_id, event_id, checkout_session.id, ticket_count
    )
    handle_ticket_availablity.delay(order.id)
    lock_key = f"lock:{event_id}:{user_id}"
    g.redis_client.set(lock_key, f", {order.id}", 30)  # Lock expires in 5 minutes
    kafka = KafkaPublisher()
    kafka.send(
        "ticket_availability",
        {
            "message": "Ticket Lock",
            "user_id": user_id,
            "event_id": event_id,
            "order_id": order.id,
        },
    )  # Ensure the message is sent immediately
    email = Email()
    email.send_email(
        "Booking Confirmed",
        ["rojesh.prajapati@outcodesoftware.com"],
        body="Ticket Booking Success",
    )

    return jsonify({"session_url": checkout_session.url, "order_id": order.id}), 200


def create_event():
    data = g.request_json_body
    user_id = g.user.id
    event_schema = EventSchema(**data)
    event = EventORM().create_event(event_schema)
    return jsonify(EventResponseSchema.from_orm(event).dict()), 201


def ticket_status(id):
    order = OrderORM().get_order(id)
    return jsonify(OrderResposeSchema.from_orm(order).dict()), 200

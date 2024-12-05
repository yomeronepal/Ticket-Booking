from flask import request, jsonify, g
import stripe
from ..database.tickets.models import Order, Ticket
from ..database import database as db
from ..utils.kafka import KafkaPublisher
from ..utils.email import Email
from ..tasks.tasks import send_email


def stripe_webhooks():
    data = g.request_json_body
    kafka = KafkaPublisher()
    event = None
    try:
        event = stripe.Event.construct_from(data, stripe.api_key)
    except ValueError as e:
        # Invalid payload
        print(e)
    if event.type == "checkout.session.completed":
        data = event.data.object
        session_id = data.id
        if data.payment_status == "paid":
            order = Order.query.filter(Order.stripe_session_id == session_id).first()
            if order:
                order.status = "Paid"
                Ticket.query.filter(Ticket.order_id == order.id).update(
                    {
                        "status": "Sold",
                    },
                    synchronize_session=False,
                )
                db.session.commit()
                send_email.delay(
                    "Booking Confirmed",
                    ["rojesh.prajapati@outcodesoftware.com"],
                    body="Ticket Booking Success",
                )
                kafka.send(
                    "payment_notifications",
                    {"message": "Payment Success", "user_id": order.user_id},
                )

    if event.type == "checkout.session.expired":
        data = event.data.object
        session_id = data.id
        order = Order.query.filter(Order.stripe_session_id == session_id).first()
        if order:
            order.status = "Failed"
            Ticket.query.filter(Ticket.order_id == order.id).update(
                {
                    "status": "Available",
                },
                synchronize_session=False,
            )
            db.session.commit()

            kafka.send(
                "ticket_availability",
                {
                    "message": "Ticket Sold",
                    "order_id": order.id,
                    "event_id": order.event_id,
                },
            )  # Ensure the message is sent immediately

    return "Success"

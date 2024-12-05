from celery import shared_task
import time
from ..database.tickets.models import Order, Ticket
from ..database import database as db
from ..utils.kafka import KafkaPublisher
from ..utils.email import Email


@shared_task(ignore_result=False)
def handle_ticket_availablity(order_id) -> int:
    time.sleep(30)  # Simulate a long-running task 300
    order = Order.query.get(order_id)
    ticket_count = Ticket.query.filter(Ticket.order_id == order_id).count()
    if order:
        if order.status == "Pending":
            Ticket.query.filter(Ticket.order_id == order_id).update(
                {
                    "status": "Available",
                },
                synchronize_session=False,
            )

            order.status = "Failed"
            db.session.commit()
            kafka = KafkaPublisher()
            kafka.send(
                "ticket_availability",
                {
                    "message": "Ticket Available",
                    "event_id": order.event.id,
                },
            )  # Ensure the message is sent immediately
            kafka.send(
                "waitlist",
                {
                    "message": f"{ticket_count} Ticket Available",
                    "event_id": order.event.id,
                },
            )  # Ensure the message is sent immediately
    return "Task Completed!"


@shared_task(ignore_result=True)
def send_email(title, recipients, body):
    email = Email()
    email.send_email(
        title,
        recipients,
        body,
    )

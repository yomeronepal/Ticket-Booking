import os
from src import create_app
from celery import Celery
from src.celery import celery_init_app
import threading
from kafka import KafkaConsumer
import json
from flask_mail import Mail

# Initialize Flask App
app = create_app()


# Create Celery instance
celery = celery_init_app(app)
TOPIC = "flask_topic"
# Email Setting
app.config["MAIL_SERVER"] = "sandbox.smtp.mailtrap.io"
app.config["MAIL_PORT"] = 2525
app.config["MAIL_USERNAME"] = "e250ef6e35714f"
app.config["MAIL_PASSWORD"] = "ee66a0efa0b836"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)


@celery.task
def long_task():
    import time

    time.sleep(10)  # Simulate a long-running task
    return "Task Completed!"


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 8000)), debug=True)

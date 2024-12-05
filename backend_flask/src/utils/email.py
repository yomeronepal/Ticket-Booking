from flask_mail import Mail, Message
from flask import Flask
import os


class Email:
    def __init__(self, app=None):
        # You can pass an app object if it's already initialized
        if app is not None:
            self.app = app
            self.client = Mail(app)
        else:
            # Initialize app if not passed
            app = Flask(__name__)
            app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
            app.config["MAIL_PORT"] = int(
                os.environ.get("MAIL_PORT", 587)
            )  # Default to 587 if not set
            app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
            app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
            app.config["MAIL_USE_TLS"] = (
                os.environ.get("MAIL_USE_TLS", "True") == "True"
            )
            app.config["MAIL_USE_SSL"] = (
                os.environ.get("MAIL_USE_SSL", "False") == "True"
            )
            self.client = Mail(app)
            self.app = app  # Store the app object

    def send_email(self, title, recipients, body):
        msg = Message(
            title,
            recipients=recipients,
            body=body,
            sender=os.environ.get("MAIL_SENDER"),
        )
        try:
            self.client.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

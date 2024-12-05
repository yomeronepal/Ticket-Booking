from flask import Flask, g, request, jsonify

from .exception_handler import handle_validation_error, handle_value_error

from .middlewares import setup_middlewares
from .database import connect_to_db
from .routes import api_routes
from config import Config
from pydantic import ValidationError
from flask_migrate import Migrate
from flask_redis import FlaskRedis
import threading
from .celery import celery_init_app
from confluent_kafka import Consumer, KafkaException, KafkaError
import os

# Create Celery instance


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Configure Redis URL
    app.config["REDIS_URL"] = os.environ.get("REDIS_URL")
    databse = connect_to_db(app)
    migrate = Migrate(app, databse)
    redis_client = FlaskRedis(app)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.environ.get("CELERY_BROKER_URL"),
            result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    app.config["CELERY_BROKER_CONNECTION_RETRY"] = True  # Retry connection on startup

    # databse.create_all()  # Creates tables based on models
    # Handler for expired keys
    def handle_expired_event(message):
        key = message["data"].decode("utf-8")
        # Trigger any desired actions, e.g., cleanup in the database, notifications, etc.

    # Function to listen for expired events
    def listen_to_expirations():
        pubsub = redis_client.pubsub()
        pubsub.psubscribe("__keyevent@0__:expired")  # Listen for expired keys on DB 0

        for message in pubsub.listen():
            if message["type"] == "pmessage":
                handle_expired_event(message)

    @app.errorhandler(ValidationError)
    def validation_error_handler(e):
        return handle_validation_error(e)

    @app.errorhandler(ValueError)
    def value_error_handler(error):
        return handle_value_error(error)

    @app.before_request
    def before_request():
        databse.create_all()  # Creates tables based on models
        # stroing database connection in global variable
        g.database = databse
        g.redis_client = redis_client
        # also see if there is any json data in req body and if yes then parse it and store it in g object
        if request.is_json:
            g.request_json_body = request.get_json()
        else:
            g.request_json_body = None

    setup_middlewares(app)
    app.register_blueprint(api_routes, url_prefix="/api")
    return app

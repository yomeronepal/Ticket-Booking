import os

ENV = os.getenv("ENV")
# DB_URL=sqlite:///app.db"
DB_URL = os.getenv("DB_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
COOKIE_NAME = os.getenv("COOKIE_NAME")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
MAIL_SENDER = os.getenv("MAIL_SENDER")
KAFKA_HOST = os.getenv("KAFKA_HOST")
REDIS_URL = os.getenv("REDIS_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

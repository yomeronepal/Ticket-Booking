from app import celery

# Start the Celery worker
celery.start(argv=["worker", "--loglevel=info"])

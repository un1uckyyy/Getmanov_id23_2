from celery import Celery
from app.core.config import settings

app = Celery(
    "worker",
    broker=settings.broker_url,
    backend=settings.broker_url,
    include=["app.tasks.binary_tasks"]
)

app.autodiscover_tasks(["app.tasks"])

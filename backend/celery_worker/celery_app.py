# celery_app.py
from app.utils.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery import Celery

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

import app.tasks

from celery import Celery
from celery.schedules import crontab

app = Celery("tasks")
app.conf.update(
    broker_url='redis://:devpassword@redis:6379/0',
    result_backend='redis://:devpassword@redis:6379/0',
    imports=('mta_tracker.tasks.tasks')
)

app.conf.beat_schedule = {
    "trigger-mta-scrape": {
        "task": "mta_tracker.scrape-mta",
        "schedule": crontab()
    }
}
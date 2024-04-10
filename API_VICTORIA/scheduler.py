from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Clima.Arable.tasks import SyncArable, SyncHistorialPred
from apscheduler.triggers.cron import CronTrigger

from utils.Console import console

scheduler = BackgroundScheduler()

scheduler.add_job(
    SyncArable,
    trigger="cron",
    hour=1,
    minute=0,
    second=0,
)
scheduler.add_job(
    SyncHistorialPred,
    trigger=CronTrigger(hour="0", minute="0", second="0", day="1"),
)
""" scheduler.add_job(
    Test,
    trigger='interval',
    seconds=5,
) """
console.log("Task sync registry")

scheduler.start()

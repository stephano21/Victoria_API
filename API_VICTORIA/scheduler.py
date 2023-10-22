from apscheduler.schedulers.background import BackgroundScheduler
from Clima.Arable.tasks import SyncArable,Test

scheduler = BackgroundScheduler()

scheduler.add_job(
    SyncArable,
    trigger='cron',
    hour=1,
    minute=0,
    second=0,
)
""" scheduler.add_job(
    Test,
    trigger='interval',
    seconds=5,
) """ 
print("Task sync registry")

scheduler.start()

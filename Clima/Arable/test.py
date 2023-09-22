from apscheduler.schedulers.background import BackgroundScheduler
from Clima.Arable.Auth import my_task  # Importa tu función de tarea

scheduler = BackgroundScheduler()
scheduler.add_job(my_task, 'interval', seconds=5)  # Ejecutar cada 30 minutos
scheduler.start()

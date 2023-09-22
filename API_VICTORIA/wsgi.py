"""
WSGI config for API_VICTORIA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application
""" apscheduler """
from apscheduler.schedulers.background import BackgroundScheduler
from Clima.Arable.tasks import SyncArable  # Importa tus tareas programadas

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_FILE'))
# Crea una instancia del planificador
scheduler = BackgroundScheduler()

# Agrega tus tareas programadas
scheduler.add_job(
    SyncArable,
    trigger='cron',
    hour=0,
    minute=0,
    second=0,
)
print("Tarea agregada correctamente")

# Inicia el planificador
scheduler.start()
application = get_wsgi_application()
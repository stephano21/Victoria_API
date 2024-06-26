from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from Clima.Arable.Auth import GetData, Login, BuidlSerializer, Current_Data, Current_Date
from Clima.serializer.IndicadorSerializer import DailyIndicadorSerializers
# Mail
from rest_framework import status
from rest_framework.response import Response
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from Predict.data.predictService import predict, update_dataset_pred

from utils.Console import console


scheduler = BackgroundScheduler()


def SyncArable():
    print(Current_Data())
    if not Current_Data():
        token = Login()
        start_time = Current_Date()
        console.log(start_time)
        if isinstance(start_time, datetime):
            data = GetData(token, start_time.date())
        else:
            data = GetData(token)
        if data == "":
            enviar_correo('Sincronización Arable',
                          'stephanochang21@gmail.com', f"Ocurrió un error con arable!")
            return Response("Ocurrió un error con arable!", status=status.HTTP_400_BAD_REQUEST)
        Format_Data = BuidlSerializer(data, "Sync_System")
        # Validar si Format_Data es un arreglo de objetos
        if not isinstance(Format_Data, list) or not all(isinstance(i, dict) for i in Format_Data):
            print(Format_Data)
        # Pasar al serializador
        DailyIndicadoresSerializers = [DailyIndicadorSerializers(
            data=data) for data in Format_Data]
        # Validar que todos los objetos esten correctos
        for serializer in DailyIndicadoresSerializers:
            if not serializer.is_valid():
                console.error(serializer.errors)

        registros_sincronizados = 0
        for serializer in DailyIndicadoresSerializers:
            if serializer.is_valid():
                serializer.save()
                registros_sincronizados += 1

        enviar_correo('Sincronización Arable', 'stephanochang21@gmail.com',
                      f"Se han sincronizado {registros_sincronizados} registros exitosamente!")
        console.log(
            f"Se han sincronizado {registros_sincronizados} registros exitosamente!")

    console.log("Los datos ya se han sincronizado!")


def Test():
    print("runing...")


def enviar_correo(asunto, destinatario, detail):
    template = get_template('mails/Mail.html')
    asunto = asunto
    mensaje = 'Este es el mensaje del correo.'
    remitente = settings.DEFAULT_FROM_EMAIL
    destinatario = destinatario  # Cambia esto al destinatario real

    # Datos para reemplazar en la plantilla HTML
    # Puedes pasar más datos según tus necesidades
    context = {'asunto': asunto, 'detalle': detail}

    try:
        # Renderizar la plantilla con los datos
        content = template.render(context)

        # Enviar el correo
        email = EmailMessage(asunto, content, remitente, [destinatario])
        email.content_subtype = 'html'  # Establecer el contenido como HTML
        email.send()
        return Response({'mensaje': 'Correo enviado exitosamente'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# TODO: Hacer un metodo que pase todas las haciendas o determinar si se puede hacer por hacienda


def SyncHistorialPred():
    fecha_mes_anterior = datetime.now() - timedelta(days=30)
    predict(1, fecha_mes_anterior)
    enviar_correo('Procesos de sincronizacion', 'stephanochang21@gmail.com',
                  f"Sincronizacion del historial de predicciones: {status}")


def SyncDatasetPred():
    status = update_dataset_pred(1)
    enviar_correo('Procesos de sincronizacion', 'stephanochang21@gmail.com',
                  f"Sincronizacion del dataset de prediccion: {status}")

from apscheduler.schedulers.background import BackgroundScheduler


from datetime import datetime
from Clima.Arable.Auth import GetData, Login, BuidlSerializer,Current_Data,Current_Date
from Clima.serializer.IndicadorSerializer import DailyIndicadorSerializers

from Clima.view.SyncView import SyncView

scheduler = BackgroundScheduler()
def SyncArable():
    print(Current_Data())
    if not Current_Data():
        token = Login()
        start_time = Current_Date()
        print(start_time)
        if isinstance(start_time, datetime):
            data = GetData(token, start_time.date())
        else:
            data = GetData(token)
        Format_Data = BuidlSerializer(data, "Sync_System")
        # Validar si Format_Data es un arreglo de objetos
        if not isinstance(Format_Data, list) or not all(isinstance(i, dict) for i in Format_Data):
            print( Format_Data)
        #Pasar al serializador
        DailyIndicadoresSerializers = [DailyIndicadorSerializers(
            data=data) for data in Format_Data]
        #Validar que todos los objetos esten correctos
        for serializer in DailyIndicadoresSerializers:
            if not serializer.is_valid():
                print( serializer.errors)

        registros_sincronizados = 0
        for serializer in DailyIndicadoresSerializers:
            if serializer.is_valid():
                serializer.save()
                registros_sincronizados += 1
        
        print( f"Se han sincronizado {registros_sincronizados} registros exitosamente!")
    
    print("Los datos ya se han sincronizado!")

def Test():
    print("runing...")   

# Agrega tus tareas programadas
scheduler.add_job(
    SyncArable,
    trigger='cron',
    hour=0,
    minute=0,
    second=0,
)
scheduler.add_job(
    Test,
    trigger='interval',
    seconds=5,
)
print("Tarea agregada correctamente file ")



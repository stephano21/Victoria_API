import pandas as pd
from datetime import datetime, timedelta
from Hacienda.models import Lectura, Lote, Planta

def ValidateLectura(data):
    required ="Este campo es requerido"
    null ="Este campo no puede ser nulo"
    try:
        # Comprobar si el diccionario request.data está vacío
        if not data:
            return "Asegurese de enviar un formulario Válido!"
        if "Id_Planta" not in data:
            return f"Id_Planta: {required}"
        if data["Id_Planta"] is None:
            print(f"Id_Planta: {null}")
            return f"Id_Planta: {null}"
        # Verificar si "FechaVisita" está en data
        if "FechaVisita" not in data:
            return f"FechaVisita: {required}"
        # Verificar si "FechaVisita" es None
        if data["FechaVisita"] is None:
            return f"FechaVisita: {null}"
        if "SyncId" not in data: 
            return f"SyncId: {required}"
        if data["SyncId"] is None:
            return f"SyncId: {null}"
        return ""
    except Exception as e:
        # En caso de error,retorna el error
        return str(e)
    
def validate_row(row, index, errors):
        headers = ['Planta','Fecha','Total','Observacion']
        print(row['Fecha'])
        has_error = False
        if not all(row[col] and not pd.isna(row[col]) for col in headers):
            missing_data = [col for col in headers if not row[col] or pd.isna(row[col])]
            errors.append(f'Datos faltantes en la fila {index+1} : {", ".join(missing_data)}')
            has_error = True
        
       
        if len(str(row['Planta']))<=1 and has_error == False:
            errors.append(f"Error en la fila {index+1} : Código de Planta no válido!")
            has_error = True
        planta_no_existe = not Planta.objects.filter(Codigo_Planta=row['Planta']).exists()
        if planta_no_existe and not has_error:
            errors.append(f"Error en la fila {index+1} {row['Planta']}: Planta no encontrada!")
            has_error = True
        # Validar que el campo 'cedula' no exista en el modelo Perfil
        #if isinstance(row['Fecha'], pd.Timestamp):
        try:
            fecha_visita = row['Fecha'].to_pydatetime()
        except ValueError as e:
            errors.append(f"Error en la fila {index+1} {row['Planta']}: El formato de fecha es invalido!")
            has_error = True
    
        if has_error:
            return errors
        print(errors)
        return

def Validate_Headers_Excel(headers,df):
    return [header for header in headers if header.lower() not in [col.lower() for col in df.columns]]

def GetIdPlanta(codigo):
    try:
        Id_Planta = Planta.objects.get(Codigo_Planta=codigo, Activo=True)
        return Id_Planta.id
    except Planta.DoesNotExist:
        # Manejar la situación donde no se encuentra ninguna planta con las condiciones dadas
        return None 
def GetIdLote(codigo):
    try:
        print(codigo)
        Id_Lote = Lote.objects.get(Codigo_Lote=codigo, Activo=True)
        print(Id_Lote.id)
        return Id_Lote.id
    except Planta.DoesNotExist:
        # Manejar la situación donde no se encuentra ninguna planta con las condiciones dadas
        return None 
        
    

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
    
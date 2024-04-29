import uuid


f = open("generateGeolotes.sql", "a")
for i in range(1, 72):
    f.write(f"INSERT INTO \"Hacienda_poligono\" (\"FillColor\", \"Id_Lote_id\", \"Activo\", \"Usuario\") VALUES ( '{'#'+str(uuid.uuid4().hex[:6])}',{i}, true, 'SYSTEM' );\n")
    #print("Geolote", i)
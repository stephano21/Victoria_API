<h1> IMPORTANTE</h1>
En linux hay que adicionar esta configuracion para usar la ruta del soket de mysql XAMPP
<code>
DATABASES = {
    'default': {
        # MySQL engine. Powered by the mysqlclient module.
        #your credentiales
        'OPTIONS': {
            'unix_socket': '/opt/lampp/var/mysql/mysql.sock',
        },
    }
}
</code>
<p>Comando para actualizar requirements.txt</p>
<code>
pip freeze > requirements.txt
</code>
<p>Comando para instalar</p>
<code>
pip install -r requirements.txt
</code>
# TIPS FOR DIPLOYMENT WITH RALYWAY
-- For linux 
ve al directorio
/opt/lampp/bin
luego ejecuta el comando de ralyway añadiendo esto al inicio "./"
./mysql -hcontainers-us-west....//resto del codigo
acto seguido pega el resaldo sql en la terminal


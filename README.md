# IMPORTANTE

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

Comando para actualizar requirements.txt

<code>
pip freeze > requirements.txt
</code>

Comando para instalar

<code>
pip install -r requirements.txt
</code>

# TIPS FOR DIPLOYMENT WITH RALYWAY
## Back ups en postgresql CLI
<code>
pg_dump -d DBname -f "/your/path/directory/file.sql"

pg_dump --data-only -d DBname -f "/your/path/directory/file.sql"
</code>

## Conexion a base de datos mysql (XAMPP) local
**En linux**
ve al directorio

<code>/opt/lampp/bin</code>

luego ejecuta el comando de <a href="https://railway.app/">ralyway</a> añadiendo esto al inicio "./"

Ejemplo


<code>./mysql -hcontainers-us-west....//resto del codigo </code>


acto seguido pega el codigo sql generado por el backup en la terminal

## Salida a intenert

> Tenia un problema con el deploy, se me ejecutava de manera local en el servidor, para ello realizé lo siguiente

cree el archivo railway.yml y cambie el comando de inicio a:

<code>
python manage.py migrate && gunicorn API_VICTORIA.wsgi</code>
Hay que eliminar esto si se usan un servidor linux
tensorflow-intel==2.15.0
 
## Setings Railway

Custom Build Command:
<code>pip install -r requirements.txt  && python manage.py migrate --noinput</code>

Custom Start Command:
<code>gunicorn API_VICTORIA.wsgi:application</code>





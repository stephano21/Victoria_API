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
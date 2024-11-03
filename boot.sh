set -eu
export PATH=~/anaconda3/bin/:~/anaconda3/condabin/:${PATH}

TIMEOUT=100
DB_HOST=postgres 
DB_PORT=5432
timeout $TIMEOUT sh -c "until nc -z $DB_HOST $DB_PORT; do sleep 1; done"

python /App/manage.py makemigrations
python /App/manage.py migrate
python /App/manage.py runserver 0.0.0.0:8080


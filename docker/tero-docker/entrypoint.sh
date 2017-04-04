#!/bin/bash

set -e
echo "-- entrypoint.sh --"
cd /tero/

if [ "$PRODUCTION" = "1" ]

then

  cp settings/circus.prod.ini circus.ini
  cp settings/prod_asgi.py settings/asgi.py
  cp settings/prod_manage.py manage.py

else

  cp settings/circus.devel.ini circus.ini
  cp settings/dev_asgi.py settings/asgi.py
  cp settings/dev_manage.py manage.py

fi

if [ ! -f /second_time ]
then
  echo "-- Creando el virtualenv --"
  if [ -d /env ]
  then
    rm -rf /env
  fi
  python3 -m venv /env
  source /env/bin/activate
  export PYTHONPATH=/env/
  export PYTHON=/env/bin/python3
  export PIP=/env/bin/pip
  echo "-- Configurado entorno virtual de python en $PYTHONPATH --"
  echo "-- El interprete de python que voy a usar es $PYTHON --"
  echo "-- Instalando requerimientos con $PIP --"
  echo "-- Installing: requirements.txt --"
  $PIP install --upgrade pip
  $PIP install -r requirements.txt
  if [ $result -eq 0 ]
  then
    touch /second_time
    echo "-- Installing: requirements.txt done --"
  else
    echo "-- Installing: requirements.txt failed --"
  fi
else
  echo "-- Requirements already installed --"
fi

case "$1" in
    runserver)
        echo "Runing server"
        source /env/bin/activate
        cd /tero/
        exec circusd circus.ini 
        ;;
    *)
        cd /
        exec "$@"
esac

exit 1

#!/bin/bash

set -e
echo "-- entrypoint.sh --"
cd /tero/

if [ ! -f /second_time ]
then
  echo "-- Installing: requirements.txt --"
  pip install -r requirements.txt
  result=$?
  rm -f /root/.cache/pip/pipdownloading
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
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    *)
        cd /
        exec "$@"
esac

exit 1

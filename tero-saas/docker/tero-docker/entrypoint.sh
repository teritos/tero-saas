#!/bin/bash

set -e
echo "-- entrypoint.sh --"
cd /tero/
cp ./settings/circus.ini.template circus.ini
mkdir ~/.aws
cp ./settings/aws.config.template ~/.aws/config 

if [ ! -f /second_time ]
then
  echo "-- Installing: requirements.txt --"
  chown -R $USER. /root/.cache/pip
  pip install --upgrade pip
  pip install -r requirements.txt
  echo "-- Installing: libtero --"
  cd /libtero
  pip install -r requirements.txt
  python ./setup.py develop
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
        cd /tero/
        exec circusd circus.ini 
        ;;
    *)
        cd /
        exec "$@"
esac

exit 1

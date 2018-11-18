#!/usr/bin/env bash


echo "Starting $NAME as `whoami`"
Port=5000
TIMEOUT=1200
pid=`ps ax | grep gunicorn | grep $Port | awk '{split($0,a," "); print a[1]}' | head -n 1`
if [ -z "$pid" ]; then
  echo "no gunicorn deamon on port $Port"
else
  kill $pid
  echo "killed gunicorn deamon on port $Port"
fi

gunicorn -w 1 --access-logfile logs/access_log.log \
--error-logfile logs/error_log.log \
--timeout $TIMEOUT \
-b 0.0.0.0:$Port app:app

tail -n 0 -f logs/*.log &
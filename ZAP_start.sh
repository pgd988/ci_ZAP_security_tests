#!/bin/sh
### BEGIN INIT INFO
# Provides:          <NAME>
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       <DESCRIPTION>
### END INIT INFO

set -e

PIDFILE=/var/run/ZAP.pid
LOGFILE=/var/log/ZAP.log

start() {
  if [ -f "$PIDFILE" ]; then
    echo 'Service already running' >&2
    return 1
  fi
  docker-compose -f /root/ZAP/docker-compose.yml up -d && \
  docker exec  kibana /usr/share/kibana/bin/kibana-plugin remove x-pack && \
  docker-compose -f /root/ZAP/docker-compose.yml stop && \
  docker-compose -f /root/ZAP/docker-compose.yml up -d
  docker-compose -f /root/ZAP/docker-compose_ZAP.yml up -d
  docker ps | grep elastic | awk {'print$1'} > $PIDFILE
}

stop() {
  if [ ! -f "$PIDFILE" ]; then
    echo 'Service not running' >&2
    return 1
  fi
  docker-compose -f /root/ZAP/docker-compose.yml stop && \
  docker-compose -f /root/ZAP/docker-compose_ZAP.yml stop && \
  docker-compose -f /root/ZAP/docker-compose.yml rm -f
  docker-compose -f /root/ZAP/docker-compose_ZAP.yml rm -f
  rm -rf $PIDFILE

}


case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $0 {start|stop}"
esac

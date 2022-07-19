#!/bin/bash
#
# init file for myproject service
#

# chkconfig: 345 99 10
# description: myproject service for Access

### BEGIN INIT INFO
# Provides: myproject
# Required-Start: $local_fs $network
# Required-Stop: $local_fs $network
# Should-Start:
# Should-Stop:
# Default-Start:
# Default-Stop:
# Short-Description: start and stop myproject service
# Description: myproject service for Access
### END INIT INFO

. /etc/init.d/functions

PIDFILE=/var/run/flask-gunicorn-auth.pid
CMD=/home/flask-gunicorn-auth/env/bin/gunicorn
SDSLIBS=/home/flask-gunicorn-auth/
ARGS="--pid $PIDFILE --bind 127.0.0.1:5000 -D app:app"


do_start() {
    echo -n "Starting flask-gunicorn-auth service: "
    export PYTHONPATH=${SDSLIBS}
    daemon --pidfile=$PIDFILE $CMD $ARGS
    RETVAL=$?
    echo
    return $RETVAL
}

do_stop() {
    echo -n "Stopping flask-gunicorn-auth service: "
    killproc -p $PIDFILE $CMD
    RETVAL=$?
    echo
    return $RETVAL
}

do_status() {
    status -p $PIDFILE $CMD
}

case "$1" in
    start)
        do_start
        RETVAL=$?
        ;;

    stop)
        do_stop
        RETVAL=$?
        ;;

    restart)
        do_stop
        do_start
        RETVAL=$?
        ;;

    status)
        do_status
        RETVAL=$?
        ;;

    *)
        echo "Usage: $0 {start|stop|status|restart}"
        RETVAL=2
esac

exit $RETVAL


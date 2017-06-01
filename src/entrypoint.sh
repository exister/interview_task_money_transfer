#!/usr/bin/env bash

set -e

DO_CONNECTION_CHECK=${DO_CONNECTION_CHECK:-true}

if [ "${DO_CONNECTION_CHECK}" = true ]; then
    for link in $(env | grep _LINK= | cut -d = -f 2 | sort | uniq)
    do
        ./wait-for-it.sh ${link}
    done
fi

LOG_LEVEL='DEBUG'

if [ "$1" == 'runserver' ]; then
    exec gosu unprivileged python manage.py runserver 0.0.0.0:8000
fi

if [ "$1" = 'uwsgi' ]; then
    chown -R unprivileged:unprivileged /media
    chown -R unprivileged:unprivileged /static
    gosu unprivileged python manage.py collectstatic --noinput
    gosu unprivileged python manage.py migrate --noinput
    gosu unprivileged python manage.py load_initial_data
    exec gosu unprivileged uwsgi --ini /app/uwsgi.ini
fi

exec "$@"

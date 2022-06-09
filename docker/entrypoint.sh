#!/bin/bash -e
mkdir -p /var/drips/static
mkdir -p /var/drips/log
mkdir -p /var/drips/conf
mkdir -p /var/drips/run

# chown drips:drips -R /var/drips/


if [[ "$*" == "worker" ]];then
    celery -A drips.config \
            worker \
            --events \
            --max-tasks-per-child=1 \
            --loglevel=${CELERY_LOGLEVEL} \
            --autoscale=${CELERY_AUTOSCALE} \
            --pidfile run/celery.pid \
            $CELERY_EXTRA


elif [[ "$*" == "beat" ]];then
    celery -A drips.config beat \
            $CELERY_EXTRA \
            --loglevel=${CELERY_LOGLEVEL} \
            --pidfile run/celerybeat.pid

elif [[ "$*" == "w2" ]];then
    django-admin db-isready --wait --timeout 60

elif [[ "$*" == "drips" ]];then
    rm -f /var/drips/run/*

    django-admin diffsettings --output unified
#    django-admin makemigrations --check --dry-run

    django-admin db-isready --wait --timeout 60
    django-admin init-setup --all --verbosity 2
#    django-admin check --deploy
    django-admin db-isready --wait --timeout 300
    echo "newrelic-admin run-program uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}"
#    exec gosu drips uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}
#    newrelic-admin run-program uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}
    uwsgi --static-map ${STATIC_URL}=${STATIC_ROOT}
else
    exec "$@"
fi

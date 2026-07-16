#!/bin/sh -e


export MEDIA_ROOT="${MEDIA_ROOT:-/var/run/app/media}"
export STATIC_ROOT="${STATIC_ROOT:-/var/run/app/static}"
export UWSGI_PROCESSES="${UWSGI_PROCESSES:-4}"
export DJANGO_SETTINGS_MODULE="drips.config.settings"
export PYTHONUNBUFFERED=1

case "$1" in
    run)
      echo "[entrypoint] Starting..."
      MAPPING=""
      if [ "${STATIC_URL}" = "/static/" ]; then
        MAPPING="--static-map ${STATIC_URL}=${STATIC_ROOT}"
      fi
      echo "[entrypoint] Running upgrade in background..."
      django-admin upgrade --all &
      exec tini -- uwsgi --http :8000 \
            -H /venv \
            --module drips.config.wsgi \
            --mimefile=/conf/mime.types \
            --uid drips \
            --gid unicef \
            --buffer-size 8192 \
            --http-buffer-size 8192 \
            --max-requests 500 \
            --max-requests-delta 50 \
            --harakiri 120 \
            --vacuum \
            $MAPPING
      ;;
    upgrade)
      django-admin upgrade --all
      ;;
    worker)
      set -- tini -- "$@"
      set -- gosu drips:unicef celery -A drips.config.celery worker --statedb /app/worker --concurrency=4 -E --loglevel=INFO
      ;;
    beat)
      set -- tini -- "$@"
      set -- gosu drips:unicef celery -A drips.config.celery beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
      ;;
    flower)
      export DATABASE_URL="sqlite://:memory:"
      set -- tini -- "$@"
      set -- gosu drips:unicef celery -A drips.config.celery flower
      ;;
esac

exec "$@"

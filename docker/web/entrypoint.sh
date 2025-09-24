#!/usr/bin/env bash
set -e

PYTHON_BIN=/usr/local/bin/python

# Wait for DB
$PYTHON_BIN /app/wait_for_db.py

echo "Running migrations..."
$PYTHON_BIN manage.py migrate --noinput

echo "Collecting static files..."
$PYTHON_BIN manage.py collectstatic --noinput

if [ "$DJANGO_CREATE_SUPERUSER" = "true" ]; then
  echo "Creating Django superuser..."
  $PYTHON_BIN manage.py createsuperuser --noinput || true
fi

echo "Starting Gunicorn..."
WEB_CONCURRENCY=${WEB_CONCURRENCY:-3}
exec gunicorn ${DJANGO_WSGI_MODULE:-myproject.wsgi}:application \
  --bind 0.0.0.0:8000 \
  --workers $WEB_CONCURRENCY \
  --timeout ${GUNICORN_TIMEOUT:-30} \
  --log-level ${GUNICORN_LOG_LEVEL:-info} \
  --access-logfile '-' \
  --error-logfile '-'

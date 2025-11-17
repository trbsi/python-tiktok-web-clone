#!/usr/bin/env bash
set -e

PYTHON_BIN=/usr/local/bin/python

# Wait for DB
$PYTHON_BIN /app/wait_for_db.py

echo "Running migrations..."
$PYTHON_BIN manage.py migrate --noinput

echo "Collecting static files..."
$PYTHON_BIN manage.py collectstatic --noinput

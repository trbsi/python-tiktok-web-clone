#!/usr/bin/env bash

# ==============================
# Deployment Script for My App
# ==============================

# Exit on any error
set -euo pipefail

# Configurable variables
CONTAINER_NAME="my-app-web"
CELERY_WORKER_CONTAINER_NAME="my-app-celery_worker"
CELERY_BEAT_CONTAINER_NAME="my-app-celery_beat"
APP_DIR="$(pwd)"   # Assumes script is run from project root
GIT_BRANCH="master"  # Change if using a different branch

# ------------------------------
# Update code from Git
# ------------------------------
echo "🔄 Updating Git repository..."
git fetch origin "$GIT_BRANCH"
git reset --hard "origin/$GIT_BRANCH"

# ------------------------------
# Install dependencies
# ------------------------------
echo "📦 Installing Python dependencies via Poetry (no virtualenv)..."
docker exec -it -u root my-app-web bash -c "export POETRY_VIRTUALENVS_CREATE=false && poetry install --no-interaction --no-ansi"


# ------------------------------
# Apply migrations
# ------------------------------
echo "🛠 Running database migrations..."
docker exec -it "$CONTAINER_NAME" python manage.py migrate

# ------------------------------
# Collect static files
# ------------------------------
echo "🖼 Collecting static files..."
docker exec -it "$CONTAINER_NAME" python manage.py collectstatic --clear --noinput

# ------------------------------
# Restart celery
# ------------------------------
cd docker &&
docker compose --env-file ../.env restart $CELERY_WORKER_CONTAINER_NAME  &&
docker compose --env-file ../.env restart $CELERY_BEAT_CONTAINER_NAME &&
docker compose --env-file ../.env restart $CONTAINER_NAME

# ------------------------------
# Run custom commands
# ------------------------------
echo "🌍 Downloading GeoIP data..."
docker exec -it "$CONTAINER_NAME" python manage.py download_geoip_command

# ------------------------------
# Deployment finished
# ------------------------------
echo "🚀 Deployment completed successfully!"

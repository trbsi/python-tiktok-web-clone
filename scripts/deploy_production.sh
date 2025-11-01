#!/usr/bin/env bash

# ==============================
# Deployment Script for My App
# ==============================

# Exit on any error
set -euo pipefail

# Configurable variables
CONTAINER_NAME="my-app-web"
CELERY_CONTAINER_NAME="my-app-celery_worker"
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
echo "📦 Installing Python dependencies via Poetry..."
docker exec -it "$CONTAINER_NAME" poetry install --no-interaction --no-ansi

# ------------------------------
# Apply migrations
# ------------------------------
echo "🛠 Running database migrations..."
docker exec -it "$CONTAINER_NAME" python manage.py migrate

# ------------------------------
# Collect static files
# ------------------------------
echo "🖼 Collecting static files..."
docker exec -it "$CONTAINER_NAME" python manage.py collectstatic --noinput

# ------------------------------
# Run custom commands
# ------------------------------
echo "🌍 Downloading GeoIP data..."
docker exec -it "$CONTAINER_NAME" python manage.py download_geoip_command

# ------------------------------
# Restart celery
# ------------------------------
cd docker && docker compose --env-file ../.env restart $CELERY_CONTAINER_NAME

# ------------------------------
# Deployment finished
# ------------------------------
echo "🚀 Deployment completed successfully!"

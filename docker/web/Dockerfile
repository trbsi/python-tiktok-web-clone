# Stage 1: build
FROM python:latest as builder

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
ENV POETRY_VERSION=2.2
RUN pip install --upgrade pip && pip install poetry==$POETRY_VERSION

# Disable Poetry virtualenvs (we want global install inside container)
RUN poetry config virtualenvs.create false

# Copy only dependency files first
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

# Stage 2: runtime
FROM python:latest

ARG UID
ARG GID

# Create group and user with the same UID/GID as host
RUN addgroup --gid ${GID} my-app-user \
    && adduser --uid ${UID} --gid ${GID} --disabled-password --gecos "" my-app-user

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev netcat-openbsd curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy entrypoint scripts
COPY docker/web/entrypoint.sh /app/entrypoint.sh
COPY docker/web/wait_for_db.py /app/wait_for_db.py
RUN chmod +x /app/entrypoint.sh

# Create directories and give permission to the UID/GID user
RUN mkdir -p /app/logs /app/staticfiles /app/uploads /app/geoip /app/celerybeat_data \
    && chown -R ${UID}:${GID} /app/logs /app/staticfiles /app/uploads /app/geoip /app/celerybeat_data

USER my-app-user

# Download GeoLite2 City database
# Dynamically determine year-month and download + extract the DB
RUN YEAR_MONTH=$(date +'%Y-%m') && \
    curl -L "https://download.db-ip.com/free/dbip-city-lite-${YEAR_MONTH}.mmdb.gz" -o /tmp/dbip.mmdb.gz && \
    gzip -d /tmp/dbip.mmdb.gz && \
    mv /tmp/dbip.mmdb /app/geoip/GeoLite-City.mmdb

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

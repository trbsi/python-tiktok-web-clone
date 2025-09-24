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
RUN poetry install --no-root --only main

# Stage 2: runtime
FROM python:latest

RUN addgroup --system app && adduser --system --ingroup app app
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev netcat curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy project code
COPY . /app

# Copy entrypoint scripts
COPY docker/web/entrypoint.sh /app/entrypoint.sh
COPY docker/web/wait_for_db.py /app/wait_for_db.py
RUN chmod +x /app/entrypoint.sh

USER app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["/app/entrypoint.sh"]

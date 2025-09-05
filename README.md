# Server setup

1. Install system dependencies

```
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip build-essential libpq-dev git curl
python3 -m pip install Django
python3 -m pip install django-environ
```

2. Install Poetry

```
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
poetry --version
```

3. Clone your GitHub project

```
cd /opt
git clone https://github.com/trbsi/python-tiktok-web-clone.git
cd python-tiktok-web-clone
```

4. Install dependencies with Poetry

```
poetry install
```

5. Activate Poetry environment

```
poetry env activate
```

6. Configure environment variables

```
cp .env.example .env
nano .env
```

7. Apply database migrations

```
python3 manage.py migrate
```

8. Collect static files (for production)

```
python3 manage.py collectstatic
```

9. Production setup (recommended)

```
poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

10. Updating your project later

```
git pull origin main
poetry install
python manage.py migrate
```
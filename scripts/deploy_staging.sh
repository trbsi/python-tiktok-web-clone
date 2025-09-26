#!/bin/bash

git pull --rebase
poetry run python manage.py seed_database --truncate
poetry run python manage.py collectstatic
sudo systemctl restart mydjango
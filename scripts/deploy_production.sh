#!/bin/bash

git pull --rebase
docker exec -it my-app-web poetry install
docker exect -it my-app-web poetry collectstatic
docker composer restart my-app-web
docker compose restart celery_worker

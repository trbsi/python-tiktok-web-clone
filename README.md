# Deployment

1. Install docker
2. Run docker
3. Restart Celery

``` 
cd docker
docker compose --env-file ../.env up -d --build
docker compose restart my-app-celery_worker
```

# Celery logs

`celery -A app worker -l info`

# Update poetry dependencies

```
docker exec -it my-app-web poetry add ...
docker compose restart my-app-web
```
# Deployment

1. Install docker
2. Run docker
3. Restart Celery

``` 
cd docker
docker compose --env-file ../.env up -d --build
docker compose restart celery_worker
```

# Update poetry dependencies

```
docker exec -it my-app-web poetry install
docker compose restart my-app-web
```
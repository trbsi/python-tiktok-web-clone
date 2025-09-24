# Deployment

1. Install docker
2. Run docker
3. Restart Celery

``` 
docker compose up -d --build
docker compose restart celery_worker
```

# Update poetry dependencies

```
docker exec -it my-app-web poetry install
docker compose restart my-app-web
```
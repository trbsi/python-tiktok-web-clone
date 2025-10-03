# Deployment

1. Create docker network
1. Install docker
1. Run docker
1. Restart Celery

``` 
docker network create my-network
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
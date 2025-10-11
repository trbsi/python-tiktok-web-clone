# Deployment

1. Create docker network
1. Install docker
1. Run docker
1. Restart Celery

``` 
make create-docker-network
make docker-build
docker compose restart my-app-celery_worker
```

*Note*: First build web image because celery worker and celery beat depend on it because of "image: my-app-web-image".
As you can see in "make docker-build"

# Celery logs

`celery -A app worker -l info`

# Update poetry dependencies

```
docker exec -it my-app-web poetry add ...
docker compose restart my-app-web
```

# Backblaze and Cloudflare

Deliver Public Backblaze B2 Content Through Cloudflare CDN

https://www.backblaze.com/docs/cloud-storage-deliver-public-backblaze-b2-content-through-cloudflare-cdn
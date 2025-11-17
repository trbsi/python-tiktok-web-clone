# Predeployment

1. Copy `.env.example` to `.env` and set up all parameters
1. Rename `docker/nginx/vhost.d/yourdomain.com` to `docker/nginx/vhost.d/your_real_domain.com`
1. Rename `docker/nginx/vhost.d/yourdomain.com_location` to `docker/nginx/vhost.d/your_real_domain.com_location`

# Deployment

1. Install docker https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
1. Install Make
1. Create docker network
1. Run docker
1. Run migration script `scripts/deploy_production.sh`

**Commands:**

For local dev add to hosts:

```
# used in NGINX_VIRTUAL_HOST
127.0.0.1 myapp.loc
# used in PHPMYADMIN_VIRTUAL_HOST
127.0.0.1 databasemyapp.loc
```

*Note*: First build web image because celery worker and celery beat depend on it because of "image: my-app-web-image".
As you can see in "make docker-build"

# Celery

## Logs

`celery -A app.celery worker -l info`

# Poetry

## Update poetry dependencies

```

docker exec -it my-app-web poetry add ...
docker compose restart my-app-web

```

# Backblaze and Cloudflare

Deliver Public Backblaze B2 Content Through Cloudflare CDN

https://www.backblaze.com/docs/cloud-storage-deliver-public-backblaze-b2-content-through-cloudflare-cdn

## SSL certificates

We don't use SSL certificates from Cloudflare because free CloudFlare limits upload to 100MB per file. Instead we use
Let's Encrypt SSL.

# LLM Chatbot

For LLM Chatbot you need to install

```
 "torch (>=2.9.0,<3.0.0)",
 "transformers (>=4.57.1,<5.0.0)",
 "peft (>=0.17.1,<0.18.0)",
 ```
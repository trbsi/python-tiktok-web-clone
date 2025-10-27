# Predeployment

1. Generate certificate in Cloudflare
    1. Put certificates in `docker/nginx/certs`
        1. yourdomain.com.crt
        1. yourdomain.com.key
        1. databasesubdomain.yourdomain.com.crt
        1. databasesubdomain.yourdomain.com.key
1. Set Cloudflare mode to be Full(Strict)
1. Copy `.env.example` to `.env` and set up all parameters
1. Rename `docker/nginx/vhost.d/yourdomain.com.example` to `docker/nginx/vhost.d/your_real_domain.com`

## Cloudflare Full (Strict) SSL Setup with jwilder/nginx-proxy

This guide explains how to configure **Cloudflare Full (Strict) SSL** for Docker services using `jwilder/nginx-proxy`.  
It covers generating Cloudflare origin certificates, placing them correctly, and configuring Cloudflare SSL mode.

---

### Generate Cloudflare Origin Certificates

1. Log in to your **Cloudflare Dashboard**.
2. Navigate to **SSL/TLS → Origin Server**.
3. Click **Create Certificate**:
    - Choose **“Let Cloudflare generate a private key and CSR”**
    - Choose **RSA 2048** (or ECC) key type
    - Set the **hostnames** you want the certificate for:
        - `yourdomain.com`
        - `databasesubdomain.yourdomain.com`
    - Set the certificate validity (default: 15 years)
4. Download the generated certificate files:
    - `.pem` (the public certificate)
    - `.key` (the private key)

---

### Set to strict mode

1. Go to SSL/TLS Settings
1. Click your domain.
1. In the menu, click SSL/TLS.
1. In the left sidebar, click Overview.
1. Click "Configure and Change SSL/TLS mode Find the section SSL/TLS encryption mode. Click Full (Strict).

# Deployment

1. Install docker https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
1. Install Make
1. Create docker network
1. Run docker
1. Migrate data
1. Collect static
1. Restart Celery

**Commands:**

``` 
sudo apt install make
make create-docker-network
make docker-build
docker compose restart my-app-celery_worker
make migrate
make collectstatic
```

For local dev add to hosts:

```
# used in NGINX_VIRTUAL_HOST
127.0.0.1 myapp.loc
# used in PHPMYADMIN_VIRTUAL_HOST
127.0.0.1 databasemyapp.loc
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
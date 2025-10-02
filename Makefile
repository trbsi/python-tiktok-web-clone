.PHONY: makemigrations, migrate, seed-database, docker-build, make-admin, collectstatic, create-docker-network

makemigrations:
	docker exec -it my-app-web python manage.py makemigrations

migrate:
	docker exec -it my-app-web python manage.py migrate

collectstatic:
	docker exec -it my-app-web python manage.py collectstatic

seed-database:
	docker exec -it my-app-web python manage.py seed_database --truncate

docker-build:
	cd docker && docker compose --env-file ../.env  up -d --build

make-admin:
	docker exec -it my-app-web python manage.py createsuperuser

create-docker-network:
	docker network create my-network

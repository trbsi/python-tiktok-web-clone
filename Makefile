.PHONY: makemigrations, migrate, collectstatic, seeddatabase, builddocker, restartweb, createsuperuser, createdockernetwork. manage

makemigrations:
	docker exec -it my-app-web python manage.py makemigrations

migrate:
	docker exec -it my-app-web python manage.py migrate

collectstatic:
	docker exec -it my-app-web python manage.py collectstatic

seeddatabase:
	docker exec -it my-app-web python manage.py seed_database local --truncate

builddocker:
	cd docker && docker compose --env-file ../.env build my-app-web && docker compose --env-file ../.env  up -d --build

restartweb:
	cd docker && docker compose --env-file ../.env restart my-app-web

createsuperuser:
	docker exec -it my-app-web python manage.py createsuperuser

createdockernetwork:
	docker network create my-network

manage:
	docker exec -it my-app-web python manage.py $(CMD)"
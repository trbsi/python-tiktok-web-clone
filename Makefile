.PHONY: makemigrations, migrate, seed_database

makemigrations:
	docker exec -it my-app-web python manage.py makemigrations

migrate:
	docker exec -it my-app-web python manage.py migrate

seed_database:
	docker exec -it my-app-web python manage.py seed_database --truncate
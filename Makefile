.PHONY: makemigrations, migrate, seed_db

makemigrations:
	docker exec -it my-app-web python manage.py makemigrations

migrate:
	docker exec -it my-app-web python manage.py migrate

seed_db:
	docker exec -it my-app-web python manage.py seed_database --truncate
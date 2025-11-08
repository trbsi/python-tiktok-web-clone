.PHONY: makemigrations, migrate, collectstatic, seeddatabase, builddocker, createsuperuser, createdockernetwork. manage, dockerssh, dockerlog, restartcontainer, truncatelogs, poetryinstall, trainchatbot

makemigrations:
	docker exec -it my-app-web python manage.py makemigrations

migrate:
	docker exec -it my-app-web python manage.py migrate

collectstatic:
	docker exec -it my-app-web python manage.py collectstatic

seeddatabase:
	docker exec -it my-app-web python manage.py seed_database_command local --truncate

createsuperuser:
	docker exec -it my-app-web python manage.py createsuperuser

trainchatbot:
	docker exec -it my-app-web python manage.py train_chatbot_command

manage:
	docker exec -it my-app-web python manage.py $(CMD)

builddocker:
	cd docker && docker compose --env-file ../.env build my-app-web && docker compose --env-file ../.env  up -d --build

restartcontainer:
	cd docker && docker compose --env-file ../.env restart $(CONTAINER)

poetryinstall:
	docker exec -it -u root my-app-web bash -c "export POETRY_VIRTUALENVS_CREATE=false && poetry install --no-interaction --no-ansi"

createdockernetwork:
	docker network create my-network

dockerssh:
	docker exec -it $(CONTAINER) /bin/bash

dockerlog:
	docker logs $(CONTAINER)

truncatelogs:
	sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' $(CONTAINER))

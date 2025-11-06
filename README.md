# django-authentication-system

A Django-based authentication service with a Dockerized dev setup (PostgreSQL + Redis + Celery). Use the commands below to build, run, and manage your local environment quickly.

## Prerequisites
- Docker and Docker Compose installed
- A `.env` file in the project root (see Environment variables below)

## Quick start
1) Build images
```sh
sudo docker compose -f docker-compose-dev.yml build
```
Builds all service images defined in compose (web, db, redis, worker).

2) Apply database migrations
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py migrate
```
Creates/updates database schema in the Postgres container.

3) Start the stack
```sh
sudo docker compose -f docker-compose-dev.yml up
```
Starts web, db, redis, and the Celery worker (logs stream in the foreground).

4) Create an admin user (optional)
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py createsuperuser
```
Interactive prompt to create a Django superuser for admin login.

## Docker commands (with brief explanations)
### Build
```sh
sudo docker compose -f docker-compose-dev.yml build
```
Build or rebuild images after changing dependencies or Dockerfile.

### Make migrations
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py makemigrations
```
Generates new migration files from your model changes.

### Migrate
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py migrate
```
Applies pending migrations to the database.

### Run project
```sh
sudo docker compose -f docker-compose-dev.yml up
```
Brings up all services (web, db, redis, worker). Add -d to run in the background.

### Install packages
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web pip install package_name
```
Installs a Python package inside the web container. Remember to pin it in `requirements.txt` and rebuild.

### Other commands
```sh
sudo docker compose -f docker-compose-dev.yml run --rm web <your_command_here>
```
Run any ad‑hoc manage.py or shell command in the web container.

## Common tasks
- Create superuser
	```sh
	sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py createsuperuser
	```

- Run tests (pytest)
	```sh
	sudo docker compose -f docker-compose-dev.yml run --rm web pytest -q
	```

- Django shell
	```sh
	sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py shell
	```

- Collect static files (if needed)
	```sh
	sudo docker compose -f docker-compose-dev.yml run --rm web python manage.py collectstatic --noinput
	```

- Stop services
	```sh
	sudo docker compose -f docker-compose-dev.yml down
	```

- Stop and remove volumes (DB reset)
	```sh
	sudo docker compose -f docker-compose-dev.yml down -v
	```
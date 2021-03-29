# KubeZephyr backend

## What for

This project is KubeZephyr backend based on fastapi+mongodb.
It can operate kubernetes resources with web API.

## Quickstart

Clone git repo and run `pip3 install`

```zsh
git clone https://github.com/zephyrxvxx7/KubeZephyr-Backend.git
cd kubezephyr-backend
pip3 install -f requirements.txt
```

Then create .env file in project root and set environment variables for application:

```zsh
touch .env
echo "PROJECT_NAME=KubeZephyr" >> .env
echo DATABASE_URL=mongo://$MONGO_USER:$MONGO_PASSWORD@$MONGO_HOST:$MONGO_PORT/$MONGO_DB >> .env
echo SECRET_KEY=$(openssl rand -hex 32) >> .env
echo ALLOWED_HOSTS='"127.0.0.1", "localhost"' >> .env
```

To run the web application in debug use:

```zsh
python3 start_server.py
```

## Deployment with Docker

You must have docker and docker-compose tools installed to work with material in this section. First, create .env file like in Quickstart section or modify .env.example. MONGO_HOST must be specified as db or modified in docker-compose.yml also. Then just run:

```zsh
docker-compose up -d
```

Application will be available on `localhost` or `127.0.0.1` in your browser.

## Web routes

All routes are available on `/docs` or `/redoc` paths with Swagger or ReDoc.

## Project structure

Files related to application are in the app directory

```zsh
models  - pydantic models that used in crud or handlers
crud    - CRUD for types from models (create new user/article/comment, check if user is followed by another, etc)
db      - db specific utils
core    - some general components (jwt, security, configuration)
api     - handlers for routes
main.py - FastAPI application instance, CORS configuration and api router including
```
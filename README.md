# ToDo Web Service
#### SkyPro student diploma work

### Stack

- django - backend
- postgresql - database
- development requirements are specified in requirements.txt

### Features

1. Authentication and User (core app):
   - VK Oauth
   - basic django authentication
   - profile update
   - password change
2. Main interface (goals app):
   - basic CRUD with filters and sorting: boards, goals, categories, comments
   - user can view items related to the boards he's member of (owner, writer or reader)
   - user can create categories, goals, comments only if he's owner/writer of the related board
   - user can update, delete only if he's owner/writer of the related board
   - user can update, delete only his comments
   - when board, category is marked as is_deleted, all child categories, goals are also marked as is_deleted
3. Telegram bot (bot app):
   - user need to verify identity using verification code
   - user could view and create goals
   - bot telegram username: @todo_sz_bot

## How to launch project in development environment

1. Create virtual environment
2. Install dependencies from requirements.dev.txt
   - `pip install -r requirements.txt`
3. Set environment variables in .env file
   - create .env file at the root
4. Launch database from deploy folder
   - `cd deploy`
   - `docker compose up postgres -d`
5. Make migrations at the root
   - `./manage.py makemigraitons`
   - `./manage.py migrate`
6. Launch project
   - `./manage.py runserver`

#### Accessing admin site

1. Create admin-user
   - `./manage.py createsuperuser`
   - set values and required fields
2. Access admin site at http://127.0.0.1:8000/admin/

## How to launch project in development with Docker-compose

1. Create .env file in deploy folder:
   - make sure to set DB_HOST to `postgres` which is a container name
2. Use docker-compose.yaml from within deploy folder
   - `cd deploy`
   - `docker compose up -d`
3. The following would be done:
   - postgresql container would start
   - migrations would apply
   - api container would start
   - front container would start

## Deploy

1. Deploy is automated with github actions. 
2. Project files used:
   - actions: .github/workflows/actions.yaml
   - compose file: deploy/docker-compose.yaml
   - env variables: deploy/.env
   - variables in compose and env files are replaced with github secrets
3. Docker hub images:
   - front: sermalenk/skypro-front:lesson-38
   - back: tsemeneev/diplom:latest
4. To add admin during first launch:
   - connect to server and access project folder
   - `docker exec -it <api container_id> /bin/bash`
   - `./manage.py createsuperuser`
5. Addresses:
   - front: http://teemz.ga
   - admin: http://teemz.ga/admin/

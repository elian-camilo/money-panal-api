## Initialize the app with uvicorn
```bash
uv run uvicorn app.main:app --reload
```

## Inicialize the db through docker
### 1. .env
Create a .env with the next variables:
```
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=
DB_HOST=

DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### 2. Docker
To be sure you have docker installed on your machine.
Then, execute this commando:
```bash
docker compose up
```
or
```bash
docker compose up -d
```
### 3. Dbeaver
If you want to use any tool for visalize your database can be use 'Dbeaver':
Instrall through: [link](https://dbeaver.io/download/)
While you db is ON, you may add a new database and put in all credential from .env
Then you can be able to see your data in real time.

### 4. Migration
But if this is the first time you inicialize this project need to make a migration from Alembic:
#### Create script migration
```bash
uv run alembic revision --autogenerate -m "<your-comment>"
```
#### Execute migration
```bash
uv run alembic upgrade head
```
> This create the database base of your project.
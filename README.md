## Use uv to magane the venv and dependencies
Install uv [here](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Now we would sync our project dependencies with:
```bash
uv sycn
```
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
Instrall through [here](https://dbeaver.io/download/).

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

## Future Improvements
Here is a simple list of things we can improve in the future:
- Admin Roles: Add an administrative role (e.g. `is_admin` or `role`) to the database and JWT token payload.
- Admin Routes: Restrict user actions so regular users cannot list all users, but administrators can.
- User Management: Build robust permission controls across all administrative routes.
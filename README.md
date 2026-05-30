# Money Panel

A minimalist personal finance manager built with Python, FastAPI, and Clean Architecture. 

Money Panel allows you to track your income, expenses, debts, and financial obligations through a clean web interface powered by Jinja2 and Bootstrap 5, while maintaining a decoupled, production-ready REST API underneath.

## Features

- **Clean Architecture**: Strict separation of concerns (Domain, Application, Infrastructure, Presentation).
- **Dual Interface**: Fully functional JSON REST API (`/api/v1`) + Server-Side Rendered Web UI (`/web`).
- **Secure Authentication**: JWT for API consumption and Cookie-based auth for the Web UI.
- **Financial Tracking**: Manage Transactions, Debts, Accounts, and Categories in one place.

## Getting Started

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### 2. Environment Setup
Create a `.env` file in the root directory of the project:
```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=money_panel
DB_PORT=5432
DB_HOST=localhost

DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
SECRET_KEY=your_secret_key_here
```

### 3. Start the Database
Run the PostgreSQL database container in the background:
```bash
docker compose up -d
```

### 4. Install Dependencies & Migrate
Use `uv` to sync your dependencies and `alembic` to apply the database schema:
```bash
uv sync
uv run alembic upgrade head
```

### 5. Run the Application
Start the FastAPI development server:
```bash
uv run uvicorn app.main:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:8000/login-page`.
2. Click on **Register** to create a new user account.
3. Log in with your new credentials.
4. Start setting up your **Accounts** and **Categories**, then begin logging your **Transactions** and **Debts**.

## Architecture Overview

This project enforces strict boundaries:
- **Routers have no DB access**: All database operations are handled by Use Cases injected with a `UnitOfWork`.
- **Decoupled Frontend**: HTML is rendered exclusively in `web_router.py`. Data is fetched internally via Use Cases, not by exposing database sessions to the templates.

## Roadmap & The Future of Money Panel

This public repository serves as a foundational demo of the architecture and core features. Moving forward, **Money Panel is transitioning into a private development phase** where it will evolve from a portfolio project into a fully-fledged financial startup.

**Upcoming Private Features:**
- **AI Financial Analysis**: Deep insights into spending habits and saving opportunities using AI.
- **Smart Receipt Capturing**: Automated expense logging through AI-powered image recognition and text extraction.
- **Auto-completion & Predictive Entry**: Smart categorization and filling of transactions based on historical data.

## Credits & Contact

Developed and architected by **Elian Camilo Angarita Sanguino**.

If you're interested in the future of this project, or just want to connect, feel free to reach out:
- [LinkedIn Profile](https://www.linkedin.com/in/elian-camilo-angarita-sanguino/)
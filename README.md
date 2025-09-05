
# Weather API 🌤️

This project is a simple **weather API** that integrates with the [7Timer API](http://www.7timer.info/) to fetch forecast data.

Users can:

- Perform **CRUD operations** on locations
- Query **daily forecasts** (min/max temperature) per location
- Manually trigger a **forecast refresh** on all stored locations

A background **cron service** keeps forecasts up to date.

## Tech-stack 🛠️

- [FastAPI](https://fastapi.tiangolo.com/) as web framework
- [PostgreSQL](https://www.postgresql.org/) as relational database
- [SQLModel](https://sqlmodel.tiangolo.com/) as ORM (built on top of [SQLAlchemy](https://www.sqlalchemy.org/))
- [Alembic](https://alembic.sqlalchemy.org/) as database migrations tool

## Pre-requirements ⚙️

Software you'll need to run this project:

- Python v3.11
- Docker + Docker Compose (if you want to run it on containers)
- PostgreSQL (if you're not using containers)

## Setup 🚀

You can run this project through Docker (recommended) or locally. Assuming you have a terminal pointing to the project root folder:

1. Copy `.env.example` → `.env` and adjust parameters.
2. Install dependencies and setup git hooks:

    ```bash
    make setup
    ````

3. Apply migrations:

   ```bash
   make migrate
   ```

4. Start containers OR start FastAPI server:

   ```bash
   make up
   ````

   or

   ```bash
   python src/run.py
   ````

5. Open the API docs at http://localhost:8000/docs (adjust the port if you've changed it)

Note: makefile has other useful commands (generate migrations, run mypy, etc.). Feel free to explore them.

## Project Structure 📂

Here's a simplified overview of the project structure:

```bash
.
├── Makefile
├── docker-compose.yml
├── .env.example
├── ...
├── migrations/             # Alembic migrations
└── src/
    ├── database.py         # Database session setup
    ├── main.py             # FastAPI app entrypoint
    ├── run.py              # App runner (uvicorn entrypoint)
    ├── ...
    ├── api/
    │   ├── location/       # Location resources (routes, controller, repo, schemas, models, entities, exceptions)
    │   └── forecast/       # Forecast resources (...)
    └── services/           # Forecast refresh service, schedulers, 7timer client, logs
```

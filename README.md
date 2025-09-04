
# Weather API 🌤️

This project is a simple **weather API** that integrates with the [7Timer API](http://www.7timer.info/) to fetch forecast data.

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [SQLModel](https://sqlmodel.tiangolo.com/) as ORM
- Handles database migrations with [Alembic](https://alembic.sqlalchemy.org/)

Users can:

- Perform **CRUD operations** on locations
- Query **daily forecasts** (min/max temperature) per location
- Manually trigger a **forecast refresh** on all stored locations

A background **cron service** keeps forecasts up to date.

## Setup 🚀

You can run this project through Docker (recommended) or locally.

1. Copy `.env.example` → `.env` and adjust parameters.
2. Install dependencies and setup git hooks:
    ```bash
    make setup
    ````
3. Start containers:
   ```bash
   make up
   ````
4. Apply migrations:
   ```bash
   make migrate
   ```
5. Open the API docs at http://localhost:8000/docs (adjust the port if you've changed it)

Note: makefile has other useful commands (generate migrations, run mypy, etc.). Feel free to explore them.

## Project Structure 📂

Here's the global structure of the project (some files were omitted):

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
    ├── run.py              # App runner (uvicorn config)
    ├── ...
    ├── api/
    │   ├── location/       # Location resources (routes, controller, repo, schemas, models, entities, exceptions)
    │   └── forecast/       # Forecast resources (...)
    └── services/           # Forecast refresh service, schedulers and 7timer client
```

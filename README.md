# UserSnack
A minimalistic pizza ordering API service built with [FastAPI](https://fastapi.tiangolo.com/) and 
[TortoiseORM](https://tortoise.github.io).

## Project Philosophy
- The project is based on the service-repository pattern. 
- The idea behind using a repository despite using a library like Tortoise-ORM is to be able to abstract 
complex database queries and do easy mocking as scale during unit tests.

## Development Setup
- Copy `.env.sample` to `.env` and set the values as necessary.

### All in Docker Compose
- Make sure `POSTGRES_HOST` value in `.env.local` to `db` and `POSTGRES_PORT` to `5432`.

Run:
```shell
docker compose up
```

### App outside of Docker
This could be useful if you need to attach a debugger to your application. As a requirement, you'd need to have 
[Poetry](https://python-poetry.org/) installed. Then you may follow the steps:

- Run Database as usual in docker or directly on your machine.
- Change the `POSTGRES_HOST` in `.env.local` to `localhost`.

```shell
export PYTHONPATH=src # you only need to set this once in your terminal session
python -m uvicorn main:app --reload
```

### Migrations
Migrations are managed with [Aerich](https://github.com/tortoise/aerich) (a migration tool by Tortoise-ORM). To 
run migrations:

```shell
# Outside docker setup
aerich upgrade

# Full docker compose setup
docker compose exec app aerich upgrade
```

### Seed Data
Some pizzas and pizza extras are available by default over the API, to seed your new database with them:

```shell
# Outside docker setup (assumes the terminal session still has the PYTHONPATH=src)
python scripts/load_fixtures.py

# Full docker compose setup
docker compose exec app python scripts/load_fixtures.py
```

Once started up, ideally, you should be able to access the project documentation over http://localhost:8000/docs 
if no custom port settings were done.

## Linting & Formatting
[Flake8](https://flake8.pycqa.org/en/latest/) is used for linting while [Black](https://github.com/psf/black) is used 
for code formatting. To run both respectively:

```shell
# Format code
./scripts/format.sh

# Lint code
./scripts/lint.sh
```

## Project Assumptions
- No authentication required.
- Scope does not include the logistics flow after ordering action.

## Improvements / Scale Production
- Phone number validation
- Add CI
- Use an container orchestration tool like k8s at scale
- Manage postgres connections with tool like PgBouncer to reduce the time spent opening and closing connections (reuse connections).
- Generate typescript client that the react FE can use. 
- Caching using Redis/memcache or similar tool.
- JSON logging 
- More unit tests for the services / repositories
- Use factories to generate test data
- Split unit and integration tests

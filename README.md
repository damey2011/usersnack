TO NOTE
- Before running migration `aerich` command, set `PYTHONPATH=src`


# Development Setup

## All in Docker Compose
```shell
docker compose up
```

## App outside of Docker
- Run Database as usual in docker or directly on your machine.
- Change the `POSTGRES_HOST` in `.env.local` to `localhost`.

```shell
export PYTHONPATH=src 
python -m app
```

## Assumptions
- No authentication required.
- Scope does not include the logistics flow after ordering action.

## Issues during setup

- **Error:**
    ```shell
    ...
    tortoise.exceptions.ConfigurationError: DB configuration not initialised. Make sure to call Tortoise.init with a valid configuration before attempting to create connections.
    ```

  - **When**: running `aerich init-db` at first setup.
  - **Solution**: Delete `migrations` folder, and run again.
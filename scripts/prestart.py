import asyncio
import logging

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from settings import settings

logger = logging.getLogger(__name__)

max_tries = 15  # 15 seconds
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def main() -> None:
    logger.info("Initializing service")

    # Only use the superuser for the check if there's a need to grant permissions to the non-superuser
    # This is only necessary in SHARED_DB_MODE where the default user did not create the tables
    engine = get_database_engine(
        settings.get_db_url(as_async=True, as_superuser=settings.SHARED_DB_MODE)
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            # Try to create session to check if DB is awake
            await session.execute(sa.text("SELECT 1"))
            logger.info("Database is available")

            if settings.SHARED_DB_MODE:
                # Grant all permissions to the database to the non-superuser
                await session.execute(
                    sa.text(f"GRANT ALL ON SCHEMA public TO {settings.DB_USER};")
                )
                await session.execute(
                    sa.text(
                        f"GRANT ALL ON ALL TABLES IN SCHEMA public TO {settings.DB_USER};"
                    )
                )
                await session.execute(
                    sa.text(
                        f"GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO {settings.DB_USER};"
                    )
                )
                await session.execute(
                    sa.text(
                        f"GRANT ALL ON DATABASE {settings.DB_NAME} TO {settings.DB_USER};"
                    )
                )
                logger.info("Granted all permissions.")

            await session.close()
        except Exception as e:
            logger.error(e)
            raise e


if __name__ == "__main__":
    asyncio.run(main())

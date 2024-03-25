import asyncio
import logging

from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)
from tortoise import Tortoise

from settings import TORTOISE_ORM

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

    await Tortoise.init(config=TORTOISE_ORM)
    connection = Tortoise.get_connection("default")

    await connection.execute_query("SELECT 1;")


if __name__ == "__main__":
    asyncio.run(main())

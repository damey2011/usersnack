import sys
from typing import Any, Dict, Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from exception_handlers import handle_object_not_found, handle_validation_exception
from exceptions import ObjectNotFoundError
from routes.v1 import v1_router
from schemas import UserSnackErrorResponse
from settings import settings

responses: Dict[Union[str, int], Dict[str, Any]] = {
    400: {"model": UserSnackErrorResponse, "description": "Bad Request"},
    404: {"model": UserSnackErrorResponse, "description": "Not Found"},
    422: {"model": UserSnackErrorResponse, "description": "Validation Error"},
}

app = FastAPI(
    responses=responses
)

register_tortoise(
    app,
    db_url=str(settings.get_postgres_dsn()),
    modules={
        "models": settings.TORTOISE_ORM_MODELS
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, handle_validation_exception)
app.add_exception_handler(ValidationError, handle_validation_exception)
app.add_exception_handler(ObjectNotFoundError, handle_object_not_found)

app.include_router(v1_router)


# DEBUG

import logging

fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)

# logger_tortoise = logging.getLogger("tortoise")
# logger_tortoise.setLevel(logging.DEBUG)
# logger_tortoise.addHandler(sh)

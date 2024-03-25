from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.staticfiles import StaticFiles
from tortoise import Tortoise

from exception_handlers import (handle_object_not_found,
                                handle_validation_exception)
from exceptions import ObjectNotFoundError
from routes.v1 import v1_router
from schemas.shared import UserSnackErrorResponse
from settings import Environment, TORTOISE_ORM, settings

responses: Dict[Union[str, int], Dict[str, Any]] = {
    400: {"model": UserSnackErrorResponse, "description": "Bad Request"},
    404: {"model": UserSnackErrorResponse, "description": "Not Found"},
    422: {"model": UserSnackErrorResponse, "description": "Validation Error"},
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await Tortoise.init(config=TORTOISE_ORM)
    yield
    await Tortoise.close_connections()


app = FastAPI(responses=responses, lifespan=lifespan, title="Usersnack")

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

app.include_router(v1_router, prefix="/v1")

if settings.ENV != Environment.PRODUCTION:
    app.mount(settings.MEDIA_PATH_PREFIX, StaticFiles(directory="media"), name="media")

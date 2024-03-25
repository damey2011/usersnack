import json

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from error_codes import UserSnackErrorCode
from exceptions import ObjectNotFoundError
from schemas.shared import UserSnackErrorResponse


def handle_validation_exception(_: Request, exception: ValidationError) -> JSONResponse:
    payload = UserSnackErrorResponse(
        code=UserSnackErrorCode.VALIDATION_ERROR,
        message=str(exception),
        details=exception.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=json.loads(payload.model_dump_json()),
    )


def handle_object_not_found(_: Request, exception: ObjectNotFoundError) -> JSONResponse:
    payload = UserSnackErrorResponse(
        code=UserSnackErrorCode.NOT_FOUND, message=str(exception), details=None
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=json.loads(payload.model_dump_json()),
    )

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from error_codes import UserSnackErrorCode

DataObject = TypeVar("DataObject", bound=BaseModel)


class PaginatedUserSnackResponse(BaseModel, Generic[DataObject]):
    results: List[DataObject]
    offset: int
    limit: int
    size: int

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }


class UserSnackErrorResponse(BaseModel):
    code: UserSnackErrorCode
    message: str
    details: Dict[str, Any] | List[Any] | None = None

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }


class Pagination(BaseModel):
    offset: int = 0
    limit: int = 10

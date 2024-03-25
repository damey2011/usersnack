from datetime import datetime, timezone
from typing import Annotated, Any, Dict, Generic, List, TypeVar

from pydantic import AfterValidator, BaseModel

from error_codes import UserSnackErrorCode

DataObject = TypeVar("DataObject", bound=BaseModel)


def validate_positive(num: int) -> int:
    if num > 0:
        return num
    raise ValueError(f"{num} is not a positive number.")


def validate_positive_or_zero(num: int) -> int:
    if num >= 0:
        return num
    raise ValueError(f"{num} is not a positive or zero value number.")


PositiveOrZeroInteger = Annotated[int, AfterValidator(validate_positive_or_zero)]
PositiveInteger = Annotated[int, AfterValidator(validate_positive)]


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
    offset: PositiveOrZeroInteger = 0
    limit: PositiveInteger = 10


class GenericOrmBasedSchema(BaseModel):
    model_config = {"from_attributes": True}

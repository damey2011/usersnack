from typing import List
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

router = APIRouter()


class DeliveryAddress(BaseModel):
    street: str
    apt: str
    city: str
    country: str


class OrderPackageIn(BaseModel):
    pizza_id: UUID
    extras: List[UUID]


class OrderIn(BaseModel):
    name: str
    contact_phones: List[str]
    delivery_address: DeliveryAddress
    packages: List[OrderPackageIn]


class OrderOut(BaseModel):
    pass


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderOut
)
def create_order(
    order: OrderIn
) -> OrderOut:
    pass

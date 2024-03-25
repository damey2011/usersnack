from decimal import Decimal
from typing import List, Self, Set
from uuid import UUID

from pydantic import BaseModel, Field

from db_models.orders import Order, OrderPackage, OrderPackageGarnish
from schemas.shared import GenericOrmBasedSchema
from schemas.snacks import PizzaExtraOut, PizzaOut


class DeliveryAddress(BaseModel):
    street: str = Field(min_length=5)
    house_number: str | None = Field(..., min_length=1)
    apt: str | None = Field(..., min_length=1)
    city: str = Field(min_length=5)
    country: str = Field(min_length=5)


class OrderPackageGarnishIn(BaseModel):
    extra_id: UUID
    quantity: int


class OrderPackageIn(BaseModel):
    pizza_id: UUID
    garnishes: List[OrderPackageGarnishIn]
    quantity: int


class OrderPackageGarnishOut(GenericOrmBasedSchema):
    extra: PizzaExtraOut
    quantity: int

    @classmethod
    def from_orm(cls, garnish: OrderPackageGarnish) -> Self:
        return cls(
            extra=PizzaExtraOut.from_orm(garnish.extra), quantity=garnish.quantity
        )


class OrderPackageOut(GenericOrmBasedSchema):
    pizza: PizzaOut
    quantity: int
    garnishes: List[OrderPackageGarnishOut]

    @classmethod
    def from_orm(cls, order_package: OrderPackage) -> Self:
        return cls(
            pizza=PizzaOut.from_orm(order_package.pizza),
            quantity=order_package.quantity,
            garnishes=[
                OrderPackageGarnishOut.from_orm(garnish)
                for garnish in order_package.package_garnishes
            ],
        )


class OrderIn(BaseModel):
    name: str = Field(min_length=5, description="Has a minimum length of 5")
    contact_phones: Set[str] = Field(min_length=1)
    delivery_address: DeliveryAddress
    packages: List[OrderPackageIn] = Field(min_length=1)


class OrderOut(GenericOrmBasedSchema, OrderIn):
    id: UUID
    total_cost: Decimal
    packages: List[OrderPackageOut]

    @classmethod
    def from_orm(cls, order: Order) -> Self:
        return cls(
            id=order.id,
            name=order.name,
            contact_phones=order.contact_phones,
            total_cost=order.total_cost,
            delivery_address=order.delivery_address,
            packages=[OrderPackageOut.from_orm(package) for package in order.packages],
        )

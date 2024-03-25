from decimal import Decimal

from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.validators import MinValueValidator

from db_models import BaseModel, M2MThroughBase
from db_models.snacks import Pizza, PizzaExtra


class Order(BaseModel):
    name = fields.CharField(max_length=100)
    contact_phones = ArrayField("VARCHAR", default=list)
    delivery_address = fields.JSONField(default=dict)
    total_cost = fields.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.00"))]
    )
    processed = fields.BooleanField(default=False)

    packages: fields.ReverseRelation["OrderPackage"]

    def __str__(self):
        return self.name


class OrderPackageGarnish(M2MThroughBase):
    """
    Can decide to put extra fields to specify other attributes, e.g. quantity of their extra
    """

    extra: fields.ForeignKeyRelation[PizzaExtra] = fields.ForeignKeyField(
        "models.PizzaExtra",
        related_name="extra_package",
    )
    order_package: fields.ForeignKeyRelation["OrderPackage"] = fields.ForeignKeyField(
        "models.OrderPackage", related_name="package_garnishes"
    )
    quantity = fields.IntField(default=1)

    class Meta:
        table = "order_package_garnish"
        unique_together = (
            "order_package",
            "extra",
        )


class OrderPackage(BaseModel):
    order: fields.ForeignKeyRelation[Order] = fields.ForeignKeyField(
        "models.Order", related_name="packages"
    )
    pizza: fields.ForeignKeyRelation[Pizza] = fields.ForeignKeyField(
        "models.Pizza",
        related_name="selected_in_orders",
    )
    extras: fields.ManyToManyRelation[PizzaExtra] = fields.ManyToManyField(
        "models.PizzaExtra",
        related_name="selected_in_orders",
        through="order_package_garnish",
        forward_key="extra_id",
        backward_key="order_package_id",
    )
    package_garnishes: fields.ReverseRelation[OrderPackageGarnish]
    quantity = fields.IntField(default=1)

    def __str__(self):
        return self.pizza

    class Meta:
        table = "order_package"

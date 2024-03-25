import uuid
from decimal import Decimal
from typing import Type

from tortoise import Model, connections
from tortoise.transactions import in_transaction

from db_models.orders import Order, OrderPackage, OrderPackageGarnish
from db_models.snacks import Pizza, PizzaExtra
from repositories.base import BaseRepository
from schemas.orders import OrderIn


class OrderRepo(BaseRepository[Order]):
    model = Order

    @staticmethod
    async def compute_cost(order_id: uuid.UUID) -> Decimal:
        connection = connections.get("default")

        def t(model: Type[Model]) -> str:
            return model.describe()["table"]

        total_extra_cost = (
            await connection.execute_query(
                f"SELECT "
                f"SUM(pe.price * opg.quantity) AS total_extra_cost "
                f"FROM {t(OrderPackageGarnish)} AS opg "
                f"JOIN {t(PizzaExtra)} AS pe "
                f"ON opg.extra_id = pe.id "
                f"JOIN {t(OrderPackage)} AS op "
                f"ON op.id = opg.order_package_id "
                f"WHERE op.order_id = '{order_id}'::uuid;"
            )
        )[1][0].get("total_extra_cost")

        total_pizza_cost = (
            await connection.execute_query(
                f"SELECT "
                f"SUM(p.price * op.quantity) AS total_pizza_cost "
                f"FROM {t(OrderPackage)} AS op "
                f"JOIN {t(Pizza)} AS p "
                f"ON op.pizza_id = p.id "
                f"WHERE op.order_id = '{order_id}'::uuid;"
            )
        )[1][0].get("total_pizza_cost")

        return total_extra_cost + total_pizza_cost

    async def save(self, order_in: OrderIn, *args, **kwargs) -> Order:
        packages_in = order_in.packages

        async with in_transaction():
            order_dict = order_in.model_dump()
            order_dict.pop("packages")

            order = await super().save(
                **order_dict, total_cost=Decimal("10.00"), **kwargs
            )

            package_garnishes = []
            order_packages = []

            for p in packages_in:
                package = OrderPackage(
                    id=uuid.uuid4(),
                    order_id=order.id,
                    pizza_id=p.pizza_id,
                    quantity=p.quantity,
                )
                order_packages.append(package)

                # Note that this won't generate nested queries since we are not hitting the database in the second loop
                for garnish in p.garnishes:
                    package_garnishes.append(
                        OrderPackageGarnish(
                            extra_id=garnish.extra_id,
                            quantity=garnish.quantity,
                            order_package_id=package.id,
                        )
                    )

            # Need to be executed sequentially as the second query depends on objects from first
            await OrderPackage.bulk_create(order_packages)
            await OrderPackageGarnish.bulk_create(package_garnishes)

            order.total_cost = await self.compute_cost(order.id)
            await order.save()

        return await self.fetch_one(
            {"id": order.id},
            prefetch=[
                "packages",
                "packages__package_garnishes",
                "packages__package_garnishes__extra",
                "packages__pizza",
                "packages__pizza__ingredients",
            ],
        )

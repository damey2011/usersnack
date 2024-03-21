from db_models.snacks import Pizza, PizzaExtra
from repositories.base import BaseRepository


class PizzaRepo(BaseRepository[Pizza]):
    model = Pizza


class PizzaExtraRepo(BaseRepository[PizzaExtra]):
    model = PizzaExtra

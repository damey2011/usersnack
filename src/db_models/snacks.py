from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField

from db_models import BaseModel, M2MThroughBase


class PizzaIngredient(BaseModel):
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "pizza_ingredient"


class PizzaRecipe(M2MThroughBase):
    """
    Can extend this model if there's a need to specify other attributes like the
    percentage of the ingredient in the Pizza, or the extent.
    e.g. If the Ingredient was "White Pepper", we could specify the spice level via
    a JSON that keeps extra attributes / just add an extra field that specifies the
    "volume" / "percentage".
    """
    pizza = fields.ForeignKeyField("models.Pizza")
    ingredient = fields.ForeignKeyField("models.PizzaIngredient")

    class Meta:
        table = "pizza_recipe"
        unique_together = ("pizza", "ingredient",)


class Pizza(BaseModel):
    name = fields.CharField(max_length=100, unique=True)
    price = fields.DecimalField(decimal_places=2, max_digits=10)
    ingredients = fields.ManyToManyField(
        "models.PizzaIngredient",
        related_name="used_in",
        through="pizza_recipe",
        forward_key="ingredient_id",
        backward_key="pizza_id"
    )
    images = ArrayField("VARCHAR", default=list)

    available_extras: fields.ManyToManyRelation["PizzaExtra"]

    def __str__(self):
        return self.name


class PizzaExtraOptions(M2MThroughBase):
    """
    Defines the pizza options that are available to a particular pizza, and if they are
    free for the Pizza
    """
    pizza = fields.ForeignKeyField("models.Pizza")
    pizza_extra = fields.ForeignKeyField("models.PizzaExtra")
    is_free = fields.BooleanField(default=False)

    class Meta:
        table = "pizza_extra_available_for"


class PizzaExtra(BaseModel):
    name = fields.CharField(max_length=100, unique=True)
    price = fields.DecimalField(decimal_places=2, max_digits=10)
    available_for: fields.ManyToManyRelation["Pizza"] = fields.ManyToManyField(
        "models.Pizza",
        related_name="available_extras",
        through="pizza_extra_available_for",
        forward_key="pizza_id",
        backward_key="pizza_extra_id"
    )

    def __str__(self):
        return self.name

    class Meta:
        table = "pizza_extra"

from uuid import uuid4

from tortoise import fields, models


class M2MThroughBase(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(M2MThroughBase):
    id = fields.UUIDField(default=uuid4, pk=True)

    class Meta:
        abstract = True

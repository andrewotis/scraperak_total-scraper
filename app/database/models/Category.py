from tortoise import Tortoise, fields
from tortoise.models import Model

class Category(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)

    class Meta:
        table = "categories"
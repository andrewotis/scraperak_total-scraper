from tortoise import Tortoise, fields
from tortoise.models import Model

class Store(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    url = fields.CharField(max_length=255)
    rakuten_url = fields.CharField(max_length=300)

    class Meta:
        table = "stores"
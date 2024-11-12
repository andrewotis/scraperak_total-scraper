from tortoise import Tortoise, fields
from tortoise.models import Model

class OfferType(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=12)


    class Meta:
        table = "offer_types"
from tortoise import Tortoise, fields
from tortoise.models import Model
# Define the database model
class Scrape(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "scrapes"
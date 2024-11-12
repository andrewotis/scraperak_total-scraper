from tortoise import Tortoise, fields
from tortoise.models import Model
# Define the database model
class Scrape(Model):
    id = fields.IntField(pk=True)
    execution_time = fields.CharField(max_length=10, null=True)
    total_workers = fields.IntField(null=True)
    total_passes = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "scrapes"
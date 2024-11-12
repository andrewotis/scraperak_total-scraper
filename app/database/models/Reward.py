from tortoise import Tortoise, fields
from tortoise.models import Model
# Define the database model
class Reward(Model):
    id = fields.IntField(pk=True)
    scrape = fields.ForeignKeyField("models.Scrape", related_name="scrape")
    store = fields.ForeignKeyField("models.Store", related_name="store")
    reward_type = fields.ForeignKeyField("models.RewardType", related_name="reward_type")
    offer_type = fields.ForeignKeyField("models.OfferType", related_name="offer_type")
    amount = fields.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        table = "rewards"
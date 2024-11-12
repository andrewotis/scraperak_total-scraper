from tortoise import Tortoise, fields
from tortoise.models import Model

class RewardCategory(Model):
    id = fields.IntField(pk=True)
    reward = fields.ForeignKeyField("models.Reward", related_name="reward")
    category = fields.ForeignKeyField("models.Category", related_name="category")


    class Meta:
        table = "reward_categories"
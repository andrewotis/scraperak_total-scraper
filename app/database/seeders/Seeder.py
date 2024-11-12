import os
from tortoise import Tortoise
from dotenv import load_dotenv
from abc import ABC, abstractmethod

class Seeder:
    def __init__(self):
       load_dotenv()
       self.DB_URL = os.getenv("DB_URL")

    async def init_seeder(self):
        await Tortoise.init(
            db_url=self.DB_URL,
            modules={'models':
                         [
                             'app.database.models.Category',
                             'app.database.models.OfferType',
                             'app.database.models.Reward',
                             'app.database.models.RewardCategory',
                             'app.database.models.RewardType',
                             'app.database.models.Scrape',
                             'app.database.models.Store'
                         ]
                     }
        )
        await Tortoise.generate_schemas()

    async def seed(self):
        await self.init_seeder()
        await self.run_queries()
        await Tortoise.close_connections()

    @abstractmethod
    async def run_queries(self):
        pass
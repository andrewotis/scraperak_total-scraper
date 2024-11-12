from app.database.seeders.Seeder import Seeder
from app.database.models.RewardType import RewardType
import asyncio

class RewardTypeSeeder(Seeder):
    async def run_queries(self):
        await RewardType.create(description="percentage")
        await RewardType.create(description="dollar")

if __name__ == "__main__":
    seeder = RewardTypeSeeder()
    asyncio.run(seeder.seed())
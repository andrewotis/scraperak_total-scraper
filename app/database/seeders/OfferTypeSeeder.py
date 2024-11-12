from app.database.seeders.Seeder import Seeder
from app.database.models.OfferType import OfferType
import asyncio

class OfferTypeSeeder(Seeder):
    async def run_queries(self):
        await OfferType.create(description="online")
        await OfferType.create(description="in-store")

if __name__ == "__main__":
    seeder = OfferTypeSeeder()
    asyncio.run(seeder.seed())
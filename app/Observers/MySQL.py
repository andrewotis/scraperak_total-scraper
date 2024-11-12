from tortoise import Tortoise
from dotenv import load_dotenv
from tortoise.exceptions import DoesNotExist

from Observers.IObserver import Observer
import asyncio
import os
from app.database.models.Store import Store
from app.database.models.Scrape import Scrape
from app.database.models.Reward import Reward
from app.database.models.OfferType import OfferType
from app.database.models.RewardType import RewardType
from app.database.models.RewardCategory import RewardCategory
from app.database.models.Category import Category

class MySQL(Observer):
    async def initialize(self):
        load_dotenv()
        db_url = os.getenv("DB_URL")
        await Tortoise.init(
            db_url=db_url,
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
        self.scrape = await Scrape.create()
        return await asyncio.sleep(0)

    async def add(self, entry):
        # algo:
        # 1:    look up/add store
        #   1a:     if there, verify we have the correct URL and rakuten links
        #   1b:     if not there, add it
        #
        # 2:    look up correct offer type
        # 3:    look up correct reward type
        # 4:    create reward
        # 5:    look up category
        #   5a:     if not there, add it
        # 6:    create reward_category record

        try:
            store = await Store.get(name__iexact=entry['store'])
            if entry['store_url'] != store.url:
                store.url = entry['store_url']
                await store.save()
            if entry['shopping_url'] != store.rakuten_url:
                store.rakuten_url = entry['shopping_url']
                await store.save()
        except DoesNotExist:
            store = await Store.create(name=entry['store'], url=entry['store_url'], rakuten_url=entry['shopping_url'])

        offer_type = await OfferType.get(description__icontains=entry['offer_type'])
        reward_type = await RewardType.get(description__icontains=entry['reward_type'])
        reward = await Reward.create(scrape=self.scrape, store=store, reward_type=reward_type, offer_type=offer_type, amount=entry['reward_amount'])

        try:
            category = await Category.get(description__icontains=entry['category'])
        except DoesNotExist:
            category = await Category.create(description=entry['category'])

        reward_category = await RewardCategory.create(reward=reward, category=category)

    def cleanup(self):
        pass
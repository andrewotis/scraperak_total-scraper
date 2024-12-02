from Observers.IObserver import Observer
from dbmodule.operations import ScrapeDB, StoreDB, OfferTypeDB, RewardTypeDB, RewardDB, CategoryDB
import logging

class MySQL(Observer):
    def initialize(self):
        self.scrape_db = ScrapeDB()
        self.app.get('logger').info("Starting MySQL Observer")

        self.store = StoreDB()
        self.offer_type = OfferTypeDB()
        self.reward = RewardDB()
        self.category = CategoryDB()
        self.reward_type = RewardTypeDB()
        scrape = self.scrape_db.create()
        self.scrape_id = scrape.id

    def add(self, entry):
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
        self.app.get('logger').info(f"entry: {entry}")
        # try:
        store = self.store.get_by_name(entry['store'], self.app.get('logger'))
        self.app.get('logger').debug(f"result of the store query: {store}. store len is {len(store)}")
        
        if len(store) == 0:
            store = self.store.create(name=entry['store'], url=entry['store_url'], rakuten_url=entry['shopping_url'])
            self.app.get('logger').debug(f"store is now {store}")
            self.app.get('logger').debug(f"store {entry['store']} was not found and was added.")
            store = self.store.get_by_name(entry['store'])
            self.app.get('logger').debug(f"This is now the results of the store query: {store}, len: {len(store)}")
        elif len(store) == 1:
            store = store[0]
        else:
            self.app.get('logger').debug(f"More than one store found for this. Please narrow your search down and try againsssssss")

        offer_type = self.offer_type.get_by_description(entry['offer_type'])
        reward_type = self.reward_type.get_by_description(entry['reward_type'])
        self.app.get('logger').debug(f"store entry is now {store}. store.id is {store['id']}")
        reward = self.reward.create(scrape_id=self.scrape_id, store_id=store.id, reward_type_id=reward_type.id, offer_type_id=offer_type.id, amount=entry['reward_amount'])

        category = self.category.get_by_description(entry['category'])
        if category is None:
            category = self.category.create(description=entry['category'])

        reward_category = self.category.add_to_reward(category.description, reward.id)

    def cleanup(self):
        if self.app.get('config').max_workers < len(self.app.get('config').urls):
            total_workers = self.app.get('config').max_workers
        else:
            total_workers = len(self.app.get('config').urls)
        self.scrape_db.update(
            self.scrape_id,
            self.app.get('timer').format_duration(),
            total_workers,
            self.app.get('counter').passes
        )
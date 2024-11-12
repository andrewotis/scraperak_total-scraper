# this class keeps an abstracted counter for # of rewards found in each category

class Counter:
    def __init__(self):
        self.data = {}
        self.cat_template = {
            'offers_found' : 0,
            'offers_processed' : 0,
            'in_store_skipped' : 0,
            'scrape_failures' : 0,
        }

        self.total_offers_found = 0
        self.scrape_failures = 0
        self.total_offers_processed = 0
        self.skipping_in_store = 0

        # data = {
        #     'accessories' : {
        #         'offers_found' : 123,
        #         'offers_processed' : 456
        #     },
        #     'electronics' : {
        #         'offers_found' : 123,
        #         'offers_processed' : 456
        #     }
        # }

    def create_category(self, category):
        self.data[category] = self.cat_template

    def increment(self, category, key, by=None):
        if category not in self.data:
            self.create_category(category)

        if key not in self.data[category]:
            self.data[category].update({
                key : 0
            })

        if by is None:
            self.data[category][key] += 1
        else:
            self.data[category][key] += by

    def mark_skipping_in_store(self, category):
        self.skipping_in_store += 1

    def mark_processed(self, category):
        if category not in self.data:
            self.create_category(category)
        self.total_offers_processed += 1

    def key_exists_or_add(self, key):
        if self.data.get(key) is None:
            self.data.update({
                key : {}
            })

    def get_scrape_failures(self):
        return self.scrape_failures

    def failed_scrape(self, category):
        self.scrape_failures += 1
        self.key_exists_or_add(category)
        update_val = 0
        if 'scrape_failures' in self.data[category]:
            current_val = self.data[category]['scrape_failures']
            update_val = current_val + 1

        self.data[category].update({
            'scrape_failures' : update_val
        })

    def report(self):
        return self.data
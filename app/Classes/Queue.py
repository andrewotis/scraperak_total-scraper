class Queue:
    def __init__(self, data, logger):
        self.items = data
        self.logger = logger
        logger.info(f"Starting queue with {len(data)} items")

    def add(self, item):
        self.logger.debug(f"Adding item to queue: {item}")
        self.items.append(item)

    def remove(self, item):
        self.logger.debug(f"Queue currently contains: {self.all()}. Removing item from queue: {item}")
        filtered = [url for url in self.items if item != url]
        self.items = filtered

    def next(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def all(self):
        return self.items
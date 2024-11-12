class ScrapeWatcher:
    def __init__(self, logger, config):
        self._observers = []
        self._data = []
        self.logger = logger
        self.config = config

    async def add_observer(self, observer):
        observer.add_logger(self.logger)
        observer.add_config(self.config)
        await observer.initialize()
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    async def add_entry(self, entry):
        self._data.append(entry)
        await self._notify_observers(entry)

    async def _notify_observers(self, entry):
        for observer in self._observers:
            await observer.add(entry)

    def _finished(self):
        for observer in self._observers:
            observer.cleanup()
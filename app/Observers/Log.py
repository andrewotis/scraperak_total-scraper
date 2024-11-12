from Observers.IObserver import Observer
import asyncio

class Log(Observer):
    async def initialize(self):
        self.logger.info("Starting Log Observer")
        return await asyncio.sleep(0)
    async def add(self, entry):
        self.logger.info(f"Entry Received: {entry}")

    def cleanup(self):
        pass
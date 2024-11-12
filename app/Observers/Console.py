from Observers.IObserver import Observer
import asyncio

class Console(Observer):
    async def initialize(self):
        self.logger.info("Starting Console Observer")
        return await asyncio.sleep(0)
    async def add(self, entry):
        print(f"Entry Received: {entry}")

    def cleanup(self):
        pass
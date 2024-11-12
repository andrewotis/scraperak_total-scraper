from Observers.IObserver import Observer
import json
import pathlib
import os
import asyncio

class File(Observer):
    async def initialize(self):
        self.logger.info("Starting File Observer")
        self.results = []
        return await asyncio.sleep(0)

    async def add(self, entry):
        self.results.append(entry)

    def cleanup(self):
        old_exists = os.path.isfile(self.config.output_file)
        if old_exists:
            os.remove(self.config.output_file)

        with open(self.config.output_file, 'w') as f:
            json.dump(self.results, f)
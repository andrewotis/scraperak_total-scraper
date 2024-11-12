from Observers.IObserver import Observer
import json
from pathlib import Path
import os
import asyncio

class File(Observer):
    async def initialize(self):
        self.filepath = Path(self.config.output_file)
        self.logger.info("Starting File Observer")
        self.results = []
        return await asyncio.sleep(0)

    async def add(self, entry):
        self.results.append(entry)

    def cleanup(self):
        old_exists = os.path.isfile(self.filepath)
        if old_exists:
            os.remove(self.filepath)

        with open(self.filepath, 'w') as f:
            json.dump(self.results, f)
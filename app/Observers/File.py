from Observers.IObserver import Observer
import json
import pathlib
import os
import asyncio

class File(Observer):
    async def initialize(self):
        self.results = []
        return await asyncio.sleep(0)

    async def add(self, entry):
        self.results.append(entry)

    def cleanup(self):
        path = str(pathlib.Path().resolve())
        old_exists = os.path.isfile(path + "../current-rewards.json")
        if old_exists:
            os.remove(path + "../current-rewards.json")

        with open(path + '../current-rewards.json', 'w') as f:
            json.dump(self.results, f)
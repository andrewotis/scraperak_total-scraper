from Observers.IObserver import Observer
import json
import os

class File(Observer):
    results = []

    def initialize(self):
        self.app.get('logger').info("Starting File Observer")
        # absolute path in context is D:\scraperak-total\scraper

    def add(self, entry):
        self.results.append(entry)

    def cleanup(self):
        path = f"output/{self.app.get('config').output_file}"

        old_exists = os.path.isfile(path)
        if old_exists:
            os.remove(path)

        os.makedirs('output', exist_ok=True)

        with open(path, "w") as json_file:
            json.dump(self.results, json_file, indent=4)
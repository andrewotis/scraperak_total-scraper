from Observers.IObserver import Observer
import asyncio

class Log(Observer):
    def initialize(self):
        self.app.get('logger').info("Starting Log Observer")

    def add(self, entry):
        self.app.get('logger').info(f"Entry Received: {entry}")

    def cleanup(self):
        pass
from Observers.IObserver import Observer
import asyncio

class Console(Observer):
    def initialize(self):
        self.app.get('logger').info("Starting Console Observer")

    def add(self, entry):
        print(f"Entry Received: {entry}")

    def cleanup(self):
        pass
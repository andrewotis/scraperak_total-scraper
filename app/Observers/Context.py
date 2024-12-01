from Observers.IObserver import Observer

class Context(Observer):
    rewards = []

    def initialize(self):
        self.app.get('logger').info("Starting Context Observer")

    def add(self, entry):
        self.rewards.append(entry)

    def cleanup(self):
        pass
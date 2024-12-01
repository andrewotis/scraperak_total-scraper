from abc import ABC, abstractmethod

class Observer(ABC):
    def add_context(self, app):
        self.app = app

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add(self, entry):
        pass

    @abstractmethod
    def cleanup(self):
        pass
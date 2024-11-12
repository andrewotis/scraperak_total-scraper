from abc import ABC, abstractmethod

class Observer(ABC):
    def add_logger(self, logger):
        self.logger = logger

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def add(self, entry):
        pass

    @abstractmethod
    def cleanup(self):
        pass
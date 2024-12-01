class ScrapeWatcher:
    def __init__(self, app):
        self._observers = []
        self._data = []
        self.app = app

    def add_observer(self, observer):
        observer.add_context(self.app)
        observer.initialize()
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def add_entry(self, entry):
        self._data.append(entry)
        self._notify_observers(entry)

    def _notify_observers(self, entry):
        for observer in self._observers:
            observer.add(entry)

    def finished(self):
        for observer in self._observers:
            observer.cleanup()
class Context:
    def __init__(self):
        self.services = {}

    def add(self, key, service):
        self.services[key] =  service

    def get(self, key):
        return self.services.get(key)

    def list(self):
        return list(self.services)

    def count(self):
        return len(self.services)
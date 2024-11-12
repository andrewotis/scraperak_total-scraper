class Queue:
    def __init__(self, data):
        self.items = data

    def add(self, item):
        self.items.append(item)

    def remove_item(self, item):
        index = self.items.index(item)
        self.items.remove(index)

    def next(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def all(self):
        return self.items
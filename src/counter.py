class Counter:
    def __init__(self):
        self._count = 0
    
    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self, value):
        self._count = value
        print(f"Count set to: {self._count}")
    
    def increment(self):
        self._count += 1
        print(f"Count: {self._count}")
    
    def get_count(self):
        return self._count
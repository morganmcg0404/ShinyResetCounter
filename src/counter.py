class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        print(f"Count: {self.count}")
    
    def get_count(self):
        return self.count
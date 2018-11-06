class Battery():

    def __init__(self, x, y, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.distances = []
        self.connections = None
        
    def __str__(self):
        return f"{self.x}, {self.y}, {self.capacity}"

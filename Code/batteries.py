class Battery():
    """
    All information belonging to a battery.
    """

    def __init__(self, x, y, capacity):
        """
        Position, capacity and distances
        to all houses from the battery.
        """
        self.x = x
        self.y = y
        self.capacity = capacity
        self.distances = []
        self.connections = []

    # def __str__(self):
    #     return f"{self.x}, {self.y}, {self.capacity}"

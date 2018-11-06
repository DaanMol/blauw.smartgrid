class House():
    """
    All information belonging to a house.
    """

    def __init__(self, x, y, output):
        """
        Position, output and distances
        to all batteries from the house.
        """
        self.x = x
        self.y = y
        self.output = output
        self.distances = []

    def __str__(self):
        return f"{self.x}, {self.y}, {self.output}, {self.distances}"

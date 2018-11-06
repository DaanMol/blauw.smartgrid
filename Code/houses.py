class House():

    def __init__(self, x, y, output):
        self.x = x
        self.y = y
        self.output = output
        self.distances = []
        self.connection = None

    def __str__(self):
        return f"{self.x}, {self.y}, {self.output}"

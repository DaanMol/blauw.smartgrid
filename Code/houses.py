import numpy as np

class House():
    """
    Class containing all information
    belonging to a house:

    - Initialisation: position, output,
                      distances to batteries,
                      connections with battery
    - Connect method
    - Print method
    """

    def __init__(self, x, y, output):
        """
        Position, output, distances
        to all batteries, connections
        list with connected battery.
        """
        self.x = x
        self.y = y
        self.output = output
        self.distances = []
        self.connection = None

    def connect(self, battery):
        """
        Connect battery to house:
        Input: battery index
        Output: self.connection
        """
        self.connection = battery

    def __str__(self):
        """
        Print statement for house object.
        """
        return f"{self.x}, {self.y}, {self.output}, {self.distances}, {self.connection}"

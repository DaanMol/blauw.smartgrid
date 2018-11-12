import numpy as np

class Battery():
    """
    Class containing all information
    belonging to a battery:

    - Initialisation: position, capacity,
                      distances to houses,
                      connections with houses
    - Connect method
    - Print method
    """

    def __init__(self, x, y, capacity):
        """
        Position, capacity, distances
        to all houses, connections list
        with connected houses.
        """
        self.x = x
        self.y = y
        self.capacity = capacity
        self.distances = np.zeros(150)
        self.connections = None

    def connect(self, house):
        """
        Connect houses to battery:
        Input: house object
        Output: updated self.connections
        """
        if self.connections:
            np.append(self.connections, house)
        else:
            self.connections = np.array(house)

    def __str__(self):
        """
        Print statement for battery object.
        """
        return f"{self.x}, {self.y}, {self.capacity}"

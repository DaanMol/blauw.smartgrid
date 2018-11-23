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

    def __init__(self, x, y, capacity, cost):
        """
        Position, capacity, distances
        to all houses, connections list
        with connected houses.
        """
        self.x = x
        self.y = y
        self.capacity = capacity
        self.max_cap = capacity
        self.distances = []
        self.connections = []
        self.cost = cost

    def connect(self, house, connect=True):
        """
        (dis)Connect houses - battery:
        Input: - House object (house)
               - Boolian (connect), disconnects
                 when False.
        Output: updated self.connections
        """
        if connect == True:
            self.connections.append(house)
        elif connect == False:
            self.connections.remove(house)

    def __str__(self):
        """
        Print statement for battery object.
        """
        return f"{self.connections}"

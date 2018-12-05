import numpy as np

# declare cost and capacity for the batteries
STANDARD_BAT = {"cost": 5000}
SMALL_BAT = {"capacity": 450, "cost":900}
MEDIUM_BAT = {"capacity": 900, "cost":1350}
LARGE_BAT = {"capacity": 1800, "cost": 1800}

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
        self.max_cap = capacity
        self.distances = []
        self.connections = []
        self.cost = STANDARD_BAT["cost"]

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

class SmallBattery():
    """
    Class containing all information
    belonging to a battery:

    - Initialisation: position, capacity,
                      distances to houses,
                      connections with houses
    - Connect method
    - Print method
    """

    def __init__(self, x, y):
        """
        Position, capacity, distances
        to all houses, connections list
        with connected houses.
        """
        self.x = x
        self.y = y
        self.capacity = SMALL_BAT["capacity"]
        self.max_cap = SMALL_BAT["capacity"]
        self.distances = []
        self.connections = []
        self.cost = SMALL_BAT["cost"]

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

class MedBattery():
    """
    Class containing all information
    belonging to a battery:

    - Initialisation: position, capacity,
                      distances to houses,
                      connections with houses
    - Connect method
    - Print method
    """

    def __init__(self, x, y):
        """
        Position, capacity, distances
        to all houses, connections list
        with connected houses.
        """
        self.x = x
        self.y = y
        self.capacity = MEDIUM_BAT["capacity"]
        self.max_cap = MEDIUM_BAT["capacity"]
        self.distances = []
        self.connections = []
        self.cost = MEDIUM_BAT["cost"]

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

class LargeBattery():
    """
    Class containing all information
    belonging to a battery:

    - Initialisation: position, capacity,
                      distances to houses,
                      connections with houses
    - Connect method
    - Print method
    """

    def __init__(self, x, y):
        """
        Position, capacity, distances
        to all houses, connections list
        with connected houses.
        """
        self.x = x
        self.y = y
        self.capacity = LARGE_BAT["capacity"]
        self.max_cap = LARGE_BAT["capacity"]
        self.distances = []
        self.connections = []
        self.cost = LARGE_BAT["cost"]

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

import numpy as np

# declare cost and capacity for the batteries
STANDARD_BAT = {"cost": 5000}
SMALL_BAT = {"capacity": 450, "cost": 900}
MEDIUM_BAT = {"capacity": 900, "cost": 1350}
LARGE_BAT = {"capacity": 1800, "cost": 1800}


class Battery():
    """
    Class containing all information
    belonging to a standard battery
    """

    def __init__(self, x, y, capacity):
        """
        Initialize position and (max) capacity
        by input.
        Add distances to houses and connections
        with houses lists.
        Define cost value by standard battery cost
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
                 when False
        Output: updated self.connections
        """
        if connect is True:
            self.connections.append(house)
        elif connect is False:
            self.connections.remove(house)


class SmallBattery():
    """
    Class containing all information
    belonging to a small battery
    """

    def __init__(self, x, y):
        """
        Initialize position by input.
        Add distances to houses and connections
        with houses lists.
        Define cost value and (max) capacity
        by small battery constants
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
                 when False
        Output: updated self.connections
        """
        if connect is True:
            self.connections.append(house)
        elif connect is False:
            self.connections.remove(house)


class MedBattery():
    """
    Class containing all information
    belonging to a medium battery
    """

    def __init__(self, x, y):
        """
        Initialize position by input.
        Add distances to houses and connections
        with houses lists.
        Define cost value and (max) capacity
        by medium battery constants
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
                 when False
        Output: updated self.connections
        """
        if connect is True:
            self.connections.append(house)
        elif connect is False:
            self.connections.remove(house)


class LargeBattery():
    """
    Class containing all information
    belonging to a large battery
    """

    def __init__(self, x, y):
        """
        Initialize position by input.
        Add distances to houses and connections
        with houses lists.
        Define cost value and (max) capacity
        by large battery constants.
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
        if connect is True:
            self.connections.append(house)
        elif connect is False:
            self.connections.remove(house)

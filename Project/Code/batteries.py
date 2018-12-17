import numpy as np

# declare cost and capacity for the batteries
CLASSES = {"STANDARD": {"cost": 5000},
           "SMALL": {"capacity": 450, "cost": 900},
           "MEDIUM": {"capacity": 900, "cost": 1350},
           "LARGE": {"capacity": 1800, "cost": 1800}}


class Battery():
    """
    Class containing all information
    belonging to a standard battery
    """

    def __init__(self, x, y, battery_type, capacity=None):
        """
        Initialize position and (max) capacity
        by input.
        Add distances to houses and connections
        with houses lists.
        Get cost and capacity from battery type (or from
        initialisation for standard battery)
        """
        self.x = x
        self.y = y
        self.distances = []
        self.connections = []
        self.cost = CLASSES[battery_type]["cost"]

        # get capacity from dictionary when not given
        if capacity:
            self.capacity = capacity
            self.max_cap = capacity
        else:
            self.capacity = CLASSES[battery_type]["capacity"]
            self.max_cap = CLASSES[battery_type]["capacity"]

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

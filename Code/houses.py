class House():
    """
    Class containing all information
    belonging to a house
    """

    def __init__(self, x, y, output):
        """
        Defines position and output
        by input.
        Initializes distances to batteries,
        connection and path variables/lists
        (style path = [[[xdata, ydata], cost], ...])
        """
        self.x = x
        self.y = y
        self.output = output
        self.distances = []
        self.connection = None
        self.path = []

    def connect(self, battery):
        """
        Connect battery to house
        Input: battery index
        Output: self.connection
        """
        self.connection = battery

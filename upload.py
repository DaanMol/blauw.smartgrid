class Grid():
    """
    """

    def __init__(self, district):
        """
        """
        self.batteries = self.load_batteries(f"Huizen&Batterijen/wijk{district}_batterijen.txt")
        self.houses = self.load_houses(f"Huizen&Batterijen/wijk{district}_huizen.csv")

    def load_batteries(self, filename):
        """
        """
        # make rooms dictionary
        batteries = []

        # read and strip file
        with open(filename, "r") as f:

    def load_houses(self, filename):
        """
        """

from houses import House
from batteries import Battery
import numpy as np


class Grid():
    """
    Grid class, contains all information
    for the grid of the district.
    """

    def __init__(self, district):
        """
        Create objects for Grid class:
        batteries and houses.
        """
        self.batteries = self.load_batteries(f"Huizen&Batterijen/wijk{district}_batterijen.txt")
        self.houses = self.load_houses(f"Huizen&Batterijen/wijk{district}_huizen.csv")
        self.distances()

    def load_batteries(self, filename):
        """
        Open .txt file of batteries.
        Read the file and get pos and cap info.
        Return list with pos and cap of batteries.
        """
        # make batteries list
        batteries_list = []

        # read and strip file
        with open(filename, "r") as f:
            text = f.read().strip().split('\n')
            for line in text:

                # take relevant parts
                line = line.split('\t')
                if line[0][0] == '[':
                    pos = line[0]
                    for char in pos:
                        if char in "[,]":
                            pos = pos.replace(char, '')
                    pos = pos.split(' ')

                    # variables
                    x = int(pos[0])
                    y = int(pos[-1])
                    capacity = float(line[-1])

                    # add Battery to batteries_list
                    batteries_list.append(Battery(x, y, capacity, 5000))

        # return list of Battery items
        return batteries_list

    def load_houses(self, filename):
        """
        Open .csv file of houses.
        Read the file and get x,y,max.output info.
        Return list with pos and max output.
        """
        # make houses list
        houses_list = []

        # read and strip file
        with open(filename, "r") as f:
            text = f.read().strip().split('\n')
            for line in text:

                # take relevant items
                line = line.split(',')
                if line[0].isdigit():

                    # variables
                    x = int(line[0])
                    y = int(line[1])
                    output = float(line[2])

                    # add House to houses_list
                    houses_list.append(House(x, y, output))

        # return list of House items
        return houses_list

    def distances(self):
        """
        Calculate distances between batteries and
        houses.
        Update distances in House and Battery objects.
        """
        # iterate over houses + batteries for coordinates
        for house in self.houses:
            x1 = house.x
            y1 = house.y
            for battery in self.batteries:
                x2 = battery.x
                y2 = battery.y

                # calculate manhatten distance and add to objects
                manhatten_distance = abs(x1 - x2) + abs(y1 - y2)
                house.distances.append(manhatten_distance)
                battery.distances.append(manhatten_distance)

    def swap(self, house_1, house_2):
        """
        Swaps the connection of two houses
        """
        # take batteries
        battery_1 = self.batteries[house_1.connection]
        battery_2 = self.batteries[house_2.connection]

        # swap the connections
        battery_1.connect(house_1, False)
        battery_2.connect(house_2, False)
        temp = house_1.connection
        house_1.connect(house_2.connection)
        house_2.connect(temp)
        battery_1.connect(house_2)
        battery_2.connect(house_1)

        # update capacity batteries
        battery_1.capacity += (house_1.output - house_2.output)
        battery_2.capacity += (house_2.output - house_1.output)

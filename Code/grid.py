from houses import House
from batteries import Battery

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
        batteries_list = np.array()

        # read and strip file
        with open(filename, "r") as f:
            text = f.read().strip().split('\n')

            # iterate over lines and append to batteries_list
            for line in text:

                # split items in line
                line = line.split('\t')

                # take relevant items
                if line[0][0] == '[':
                    pos = line[0]

                    # remove signs from pos
                    for char in pos:
                        if char in "[,]":
                            pos = pos.replace(char, '')
                    pos = pos.split(' ')

                    # variables
                    x = int(pos[0])
                    y = int(pos[-1])
                    capacity = float(line[-1])

                    # add Battery to batteries_list
                    np.append(batteries_list, Battery(x, y, capacity))

        # return list of Battery items
        return batteries_list


    def load_houses(self, filename):
        """
        Open .csv file of houses.
        Read the file and get x,y,max.output info.
        Return list with pos and max output.
        """
        # make houses list
        houses_list = np.array()

        # read and strip file
        with open(filename, "r") as f:
            text = f.read().strip().split('\n')

            # iterate over lines and append to houses_list
            for line in text:

                # split items in line
                line = line.split(',')

                # take relevant items
                if line[0].isdigit():

                    # variables
                    x = int(line[0])
                    y = int(line[1])
                    output = float(line[2])

                    # add House to houses_list
                    np.append(houses_list, House(x, y, output))

        # return list of House items
        return houses_list


    def distances(self):
        """
        Calculate distances between batteries and
        houses.
        Update distances in House and Battery objects.
        """
        # iterate over houses and batteries
        for house in self.houses:

            # coordinates house
            x1 = house.x
            y1 = house.y

            for battery in self.batteries:

                # coordinates battery
                x2 = battery.x
                y2 = battery.y

                # calculate manhatten distance and add to objects
                manhatten_distance =  abs(x1 - x2) + abs(y1 - y2)
                np.append(house.distances, manhatten_distance)
                np.append(battery.distances, manhatten_distance)

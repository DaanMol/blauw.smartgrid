import matplotlib.pyplot as plt

class Grid():
    """
    Grid class, contains all information
    for the grid of the district.
    """

    def __init__(self, district):
        """
        Create objects for Grid class:
        batteries and houses
        """
        self.batteries = self.load_batteries(f"Huizen&Batterijen/wijk{district}_batterijen.txt")
        self.houses = self.load_houses(f"Huizen&Batterijen/wijk{district}_huizen.csv")
        self.distances_battery = self.distances()

    def load_batteries(self, filename):
        """
        Open .txt file of batteries
        Read the file and get pos and cap info
        Return list with pos and cap of batteries
        """
        # make batteries list
        batteries_list = []
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
                    # add list to batteries_list
                    batteries_list.append([int(pos[0]), int(pos[-1]),
                                           float(line[-1])])
        # return list of batteries
        return batteries_list

    def load_houses(self, filename):
        """
        Open .csv file of houses
        Read the file and get x,y,max.output info
        Return list with pos and max output
        """
        # make houses list
        houses_list = []
        # read and strip file
        with open(filename, "r") as f:
            text = f.read().strip().split('\n')
            # iterate over lines and append to houses_list
            for line in text:
                # split items in line
                line = line.split(',')
                # take relevant items
                if line[0].isdigit():
                    # add list to houses_list
                    houses_list.append([int(line[0]), int(line[1]),
                                        float(line[2])])
        # return list of houses
        return houses_list

    def distances(self):
        """
        Calculate manhatten distances between
        houses and every battery, add these
        distances to a dictionary.
        Return list with a distance dictionary
        for every battery.
        """
        # list for distance dictionaries
        items = []
        # iterate over batteries
        for battery in self.batteries:
            # dictionary for distances
            distances = {}
            # variables in battery
            x1, y1, cap1 = battery
            # iterate over houses
            for house in self.houses:
                # variables in house
                x2, y2, cap2 = house
                # calculate manhatten distance
                d = abs(x1 - x2) + abs(y1 - y2)
                # add to distances dictionary
                distances[d] = house
            # add distances dictionary to items dictionary
            items.append(distances)
        # return list of dictionaries
        return items

    def plot_grid(self):
        """
        Make a picture of the Grid
        """
        # add houses to image
        for house in self.houses:
            plt.plot(house[0], house[1], 'ro')
        # add batteries to image
        for battery in self.batteries:
            plt.plot(battery[0], battery[1], 'bo')
        # show image
        plt.show()

# run
if __name__ == "__main__":
    grid = Grid(1)

    # print(f"batteries:{grid.batteries}")
    # print(f"houses:{grid.houses}")
    # grid.plot_grid()

    # total_battery = 0
    # total_houses = 0
    # for i in grid.batteries:
    #     total_battery += i[2]
    # for i in grid.houses:
    #     total_houses += i[2]
    # print(total_battery - total_houses)

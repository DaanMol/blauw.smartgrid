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


# run
if __name__ == "__main__":
    grid = Grid(2)
    print(f"batteries:{grid.batteries}")
    print(f"houses:{grid.houses}")

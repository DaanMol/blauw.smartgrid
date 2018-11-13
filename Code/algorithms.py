from grid import Grid
from actions import Plots
from bokeh import Bokeh
import matplotlib.pyplot as plt
import random
import time


class Algorithm():
    """
    Class containing algorithms.
    """

    def __init__(self, district):
        """
        Loading the grid information.
        Input: district number (district)
        Output: Grid object containing:
                - List with houses objects
                - List with battery objects
        """
        self.grid = Grid(district)

    def algorithm_0(self, already_used=[]):
        """
        Connects houses to batteries, only
        taking capacity into mind.
        """
        # list with connected houses
        used = already_used

        # iterate over batteries and houses
        for battery in self.grid.batteries:
            for house in self.grid.houses:
                # when house fits inside capacity add house
                if house not in used and battery.capacity - house.output > 0:
                    battery.connect(house)
                    battery.capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))

        # error message when not all houses connected
        if len(used) < 150:
            self.error_message(used)

    def algorithm_1(self, already_used=[]):
        """
        Iterates over batteries, adds
        the closest houses to the current
        battery.
        """
        # list of connected houses
        used = already_used

        # iterate over batteries
        for battery in self.grid.batteries:
            # sort houses by distances to current battery
            distances = battery.distances
            houses = self.grid.houses
            sorted_houses = [x for (y, x) in sorted(zip(distances, houses),
                                                    key=lambda pair: pair[0])]
            # iterate over the sorted houses
            for house in sorted_houses:
                # add the house when it fits in the capacity
                if not house in used and battery.capacity - house.output > 0:
                    battery.connect(house)
                    battery.capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))

        # error message when not all houses connected
        if len(used) < 150:
            self.error_message(used)

    def algorithm_2(self):
        """
        Iterates over houses sorted by the
        difference between the two closest batteries.
        When difference equals zero, makes use of
        best fit bin packing.
        """
        # lists for connected houses and relative distances
        used = []
        relatives = []

        # sort houses by the difference between two closest batteries
        for house in self.grid.houses:
            difference = sorted(house.distances)[1] - sorted(house.distances)[0]
            relatives.append(difference)
        sorted_houses = [x for (y, x) in sorted(zip(relatives, self.grid.houses),
                                                key=lambda pair: pair[0], reverse=True)]
        # iterate over sorted houses
        for house in sorted_houses:
            # sort the batteries by distance
            sorted_bat = [x for (y, x) in
                          sorted(zip(house.distances, self.grid.batteries),
                                 key=lambda pair: pair[0])]
            # iterate over the batteries
            for i in range(len(sorted_bat)):
                batt_now = sorted_bat[i]
                batt_next = sorted_bat[i + 1]

                # best fit bin packing or capacity too small (skip battery)
                if (batt_next.capacity - batt_now.capacity > 0 and
                        batt_next.capacity < batt_now.capacity) or \
                        batt_now.capacity - house.output < 0:
                    if i < 3:
                        continue
                    else:
                        batt_now = batt_next

                # update
                batt_now.capacity -= house.output
                batt_now.connect(house)
                house.connect(self.grid.batteries.index(batt_now))
                used.append(house)
                break

        # error message when not all houses connected
        if len(used) < 150:
            self.error_message(used)

    def error_message(self, used):
        """
        Error message when houses not connected
        """
        print(f"Error: {150 - len(used)} houses not connected.")

    def hillclimber(self, boundary):
        """
        Checks if swapping two house-battery
        connections is possible and decreases the
        total cost. (does this until nothing changes)
        Swaps when favourable.
        """
        # take length houses list
        length = len(self.grid.houses)

        # continue until nothing changed
        changed = boundary
        while changed is not 0:
            changed -= 1

            # take two random house index
            index_1 = int(random.uniform(0, 149))
            index_2 = int(random.uniform(0, 149))

            # take the two houses and their batteries
            house_1 = self.grid.houses[index_1]
            house_2 = self.grid.houses[index_2]
            battery_1 = self.grid.batteries[house_1.connection]
            battery_2 = self.grid.batteries[house_2.connection]

            # skip when both on same battery
            if battery_1 == battery_2:
                continue

            # skip when swapping is not possible capacity wise
            if battery_1.capacity - house_1.output + house_2.output < 0:
                continue
            if battery_2.capacity - house_2.output + house_1.output < 0:
                continue

            # calculate old and new distances
            dist_1 = house_1.distances[house_1.connection]
            dist_2 = house_2.distances[house_2.connection]
            dist_1_new = house_1.distances[house_2.connection]
            dist_2_new = house_2.distances[house_1.connection]

            # swap when total distance decreases
            if dist_1 + dist_2 > dist_1_new + dist_2_new:
                self.grid.swap(house_1, house_2)
                changed = boundary

    def k_means(self):
        """
        Apply a K-means algorithm to the grid
        Currently neglects the capacity of the battery
        """
        changes = 1
        iterations = 0
        old_connection = None
        while changes > 0:
            iterations += 1
            changes = 0

            # clear battery connectoins
            for battery in self.grid.batteries:
                battery.connections = []
            for house in self.grid.houses:
                distances = house.distances
                batteries = self.grid.batteries
                sorted_batteries = [x for (y, x) in sorted(zip(distances, batteries),
                                                           key=lambda pair: pair[0])]
                if house.connection != self.grid.batteries.index(sorted_batteries[0]):
                    changes += 1
                house.connect(self.grid.batteries.index(sorted_batteries[0]))

                # check if the connections have changed
                for battery in self.grid.batteries:
                    if sorted_batteries[0] == battery:
                        battery.connect(house)

            # reposition battery according to average xy
            for battery in self.grid.batteries:
                x, y = 0, 0
                for house in battery.connections:
                    x += house.x
                    y += house.y
                battery.x = round(x / len(battery.connections))
                battery.y = round(y / len(battery.connections))

            # clear distances and calculate new ones
            for house in self.grid.houses:
                house.distances = []
            for battery in self.grid.batteries:
                battery.distances = []
            self.grid.distances()

        print('iterations: ', iterations)


# run
if __name__ == "__main__":
    # create algorithm Object
    algo = Algorithm(1)

    # create plots Object
    plot = Plots(algo.grid)

    # create bokeh object
    bokeh = Bokeh(algo.grid)
    bokeh.simple_plot()

    """Algorithms"""
    # algo.algorithm_0()
    # algo.algorithm_1()
    # algo.algorithm_2()
    # cost_1 = plot.cost()
    # print("start =", cost_1)

    # algo.hillclimber(10000000)
    # cost_2 = plot.cost()
    # print("improvement =", cost_1 - cost_2)
    # print("end =", cost_2)

    # algo.k_means()

    """Plots"""
    # plots
    # plot.line_figure()
    # plot.x_or_y_first(False)
    # plot.random_simulation(False)

    # calculate cost
    # print("cost =", plot.cost())

    # show plots
    # plt.show()

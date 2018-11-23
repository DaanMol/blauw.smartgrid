from grid import Grid
from actions import Plots
# from bokeh import Bokeh
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

    def random_cap(self):
        """
        Connects houses to batteries, only
        taking capacity into mind.
        """
        # list with connected houses
        used = []

        # random sorted list houses
        random.shuffle(self.grid.houses)

        # iterate over batteries and houses and add house when output fits cap
        for battery in self.grid.batteries:
            for house in self.grid.houses:
                if house not in used and battery.capacity - house.output > 0:
                    battery.connect(house)
                    battery.capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))

        # fix that sh*@!$
        not_used = set(used).symmetric_difference(set(self.grid.houses))
        if len(not_used) > 0:
            self.capacity_fixer(not_used)

    def proximity_first(self):
        """
        Iterates over batteries, adds
        the closest houses to the current
        battery.
        """
        # list of connected houses
        used = []

        # iterate over batteries sort houses by distances
        for battery in self.grid.batteries:
            distances = battery.distances
            houses = self.grid.houses
            sorted_houses = self.sort_zip(distances, houses)

            # iterate over the sorted houses and add when output fits capacity
            for house in sorted_houses:
                if not house in used and battery.capacity - house.output > 0:
                    battery.connect(house)
                    battery.capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))

        # fix that sh*@!$
        not_used = set(used).symmetric_difference(set(self.grid.houses))
        if len(not_used) > 0:
            self.capacity_fixer(not_used)

    def priority_first(self):
        """
        Iterates over houses sorted by the
        difference between the two closest batteries.
        When houses not used, use capacity_creator
        """
        # lists for connected houses and relative distances
        not_used = []
        relatives = []
        used = []

        # sort houses by the difference between two closest batteries
        for house in self.grid.houses:
            difference = sorted(house.distances)[1] - sorted(house.distances)[0]
            relatives.append(difference)
        sorted_house = self.sort_zip(relatives, self.grid.houses, True)

        # iterate over sorted houses and sort batteries by distance
        for house in sorted_house:
            sorted_bat = [x for (y, x) in
                          sorted(zip(house.distances, self.grid.batteries),
                                 key=lambda pair: pair[0])]
            sorted_dis = sorted(house.distances)

            # iterate over the batteries
            for i in range(len(sorted_bat)):
                batt_now = sorted_bat[i]

                # check current capacity
                if batt_now.capacity - house.output < 0:
                    if i == len(sorted_bat) - 1:
                        not_used.append(house)
                    continue

                # update
                batt_now.capacity -= house.output
                batt_now.connect(house)
                house.connect(self.grid.batteries.index(batt_now))
                used.append(house)
                break

        # fix that sh*@!$
        if len(not_used) > 0:
            self.capacity_fixer(not_used)

    def capacity_fixer(self, not_used):
        """
        Creates space for not used houses by
        swapping big capacities with small
        capacities whenever possible.
        """
        # iterate over not used houses
        for house in not_used:
            offset = 0
            enough_space = False

            # continue until enough space for the house
            while not enough_space:
                needed_space = house.output
                available_capacity = []

                # sort batteries by avaiable capacity (biggest first)
                for battery in self.grid.batteries:
                    available_capacity.append(battery.capacity)
                sorted_batt = self.sort_zip(available_capacity,
                                            self.grid.batteries, True)

                # iterate over sorted batteries and list outputs houses
                for battery in sorted_batt[1:]:
                    outputs_1 = []
                    for i in sorted_batt[0].connections:
                        outputs_1.append(i.output)
                    outputs_2 = []
                    for i in battery.connections:
                        outputs_2.append(i.output)

                    # sort houses biggest battery big to small
                    # sort houses second biggest battery small to big
                    sorted_house_1 = self.sort_zip(outputs_1, sorted_batt[0].connections, True)
                    sorted_house_2 = self.sort_zip(outputs_2, battery.connections)

                    # check if swapping the houses is possible and creates
                    # enough space (incuded offset when needed)
                    for house_1 in sorted_house_1:
                        for house_2 in sorted_house_2:
                            output_diff = house_1.output - house_2.output
                            if output_diff - (needed_space - offset - \
                                              sorted_batt[0].capacity) > 0 and \
                               battery.capacity - output_diff > 0:
                                self.grid.swap(house_1, house_2)

                                # check if enough space
                                if sorted_batt[0].capacity > needed_space:
                                    enough_space = True
                                break

                        # if enough space stop the for loops
                        if enough_space:
                            break
                    if enough_space:
                        break

                # connect house when possible, else increase offset and retry
                if enough_space:
                    house.connect(self.grid.batteries.index(sorted_batt[0]))
                    sorted_batt[0].connect(house)
                    sorted_batt[0].capacity -= house.output
                else:
                    offset += 10

    def error_message(self, used):
        """
        Error message when houses not connected
        """
        print(f"Error: {150 - len(used)} houses not connected.")

    def sort_zip(self, in1, in2, reverse=False):
        """
        Sorts in2 by in1 smallest to
        biggest values.
        If reverse == true biggest to
        smallest.
        """
        sorting = [x for (y, x) in sorted(zip(in1, in2),
                                                 key=lambda pair: pair[0],
                                                 reverse=reverse)]
        return sorting

    def profitable_swap(self, index_1, index_2):
        """
        Checks if swapping two house-battery
        connections is possible and decreases the
        total cost.
        Swaps when favourable.
        """
        # take the two houses and their batteries
        house_1 = self.grid.houses[index_1]
        house_2 = self.grid.houses[index_2]
        battery_1 = self.grid.batteries[house_1.connection]
        battery_2 = self.grid.batteries[house_2.connection]

        # skip when both on same battery
        if battery_1 == battery_2:
            return False

        # skip when swapping is not possible capacity wise
        if battery_1.capacity + house_1.output - house_2.output < 0:
            return False
        if battery_2.capacity + house_2.output - house_1.output < 0:
            return False

        # calculate old and new distances
        dist_1 = house_1.distances[house_1.connection]
        dist_2 = house_2.distances[house_2.connection]
        dist_1_new = house_1.distances[house_2.connection]
        dist_2_new = house_2.distances[house_1.connection]

        # swap when total distance decreases
        if dist_1 + dist_2 > dist_1_new + dist_2_new:
            self.grid.swap(house_1, house_2)
            return True
        return False

    def random_hillclimber(self, lineplot=False):
        """Random input for profitable_swap"""
        swapped = True

        # list for plot
        if lineplot:
            plot = Plots(self.grid)
            cost_list = []

        # climb until nothing changes
        while swapped == True:
            swapped = False

            # create two random index lists
            index_list_1 = list(range(1, 150))
            index_list_2 = list(range(1, 150))
            random.shuffle(index_list_1)
            random.shuffle(index_list_2)

            # try all possibilities
            for index_1 in index_list_1:
                for index_2 in index_list_2:
                    if self.profitable_swap(index_1, index_2):
                        swapped = True
                    if lineplot:
                        cost_list.append(plot.cost())
        if lineplot:
            plt.plot(cost_list)

    def k_means(self):
        """
        Apply a K-means algorithm to the grid
        Currently neglects the capacity of the battery
        """
        changes = 1
        iterations = 0
        old_connection = None
        for i in range(20):
            iterations += 1
            changes = 0
            used = []
            not_used = []

            # clear battery connectoins
            for battery in self.grid.batteries:
                battery.connections = []
                battery.capacity = battery.max_cap

            for house in self.grid.houses:
                distances = house.distances
                batteries = self.grid.batteries
                sorted_batteries = self.sort_zip(distances, batteries)
                if not house.connection == self.grid.batteries.index(sorted_batteries[0]):
                    changes += 1

                # select closest battery
                # check if battery capacity is sufficient
                # else select next closest battery
                count = 0
                for battery in sorted_batteries:
                    count += 1
                    if (battery.capacity - house.output) > 0:
                        battery.capacity -= house.output
                        house.connect(self.grid.batteries.index(battery))
                        used.append(house)
                        battery.connect(house)
                        break
                    if count == 5:
                        not_used.append(house)

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

        # print('iterations: ', iterations)

        if len(used) < 150:
            self.capacity_fixer(not_used)


# run
if __name__ == "__main__":
    # create algorithm Object
    algo = Algorithm(1)

    # create plots Object
    plot = Plots(algo.grid)

    # create bokeh object
    # bokeh = Bokeh(algo.grid)
    # bokeh.simple_plot()

    """Algorithms"""
    algo.random_cap()
    # algo.proximity_first()
    # # algo.priority_first()
    # cost_1 = plot.cost()
    # print("start =", cost_1)
    #
    algo.random_hillclimber()
    # for i in algo.grid.batteries:
    #     print(i.capacity)
    # cost_2 = plot.cost()
    # print("improvement =", cost_1 - cost_2)
    # print("end =", cost_2)

    # algo.k_means()
    # algo.house_to_bat()

    # cost = []
    # for i in range(100000):
    #     algo = Algorithm(1)
    #     plot = Plots(algo.grid)
    #     algo.random_cap()
    #     # algo.k_means()
    #     # algo.priority_first()
    #     # print(plot.cost())
    #     # algo.random_hillclimber()
    #     curr_cost = plot.cost()
    #     cost.append(curr_cost)
    #     if i%500 == 0:
    #         print("check", i/500)
    # plt.figure()
    # plt.hist(cost, bins=100)
    # print(cost)
    # print("min =", min(cost))
    # print("max =", max(cost))
    # with open("text_info_random.txt", 'w') as f:
    #     for i in cost:
    #         f.write(f"{i}\n")
    # algo.random_hillclimber(100000)
    # plot = Plots(list)

    """Plots"""
    # plots
    plot.line_figure("hillclimber")
    # plot.x_or_y_first(False, "hillclimber")
    # plot.random_simulation(False, "hillclimber")

    # calculate cost
    # print("cost =", plot.cost())

    # show plots
    plt.show()

    # plot.plot_histograms_bokeh()
    # plot.plot_grid_bokeh()
    # plot.plot_matrix_bokeh()

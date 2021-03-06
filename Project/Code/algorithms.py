from grid import Grid
from actions import Plots
import matplotlib.pyplot as plt
import random
import math
import copy
from batteries import Battery


class Algorithm():
    """
    Class containing algorithms.
    """

    def __init__(self, district, setting):
        """
        Loading the grid information.
        Input: district number (district)
        Output: Grid object containing:
                - List with houses objects
                - List with battery objects
        """
        self.grid = Grid(district, setting)
        self.previous = []

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

        # fix the capacity if one ore more houses are left unconnected
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
                if house not in used and battery.capacity - house.output > 0:
                    battery.connect(house)
                    battery.capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))

        # fix the capacity if one ore more houses are left unconnected
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
            difference = sorted(house.distances)[1] - \
                         sorted(house.distances)[0]
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

        # fix the capacity if one ore more houses are left unconnected
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
                    sorted_house_1 = self.sort_zip(outputs_1,
                                                   sorted_batt[0].connections,
                                                   True)
                    sorted_house_2 = self.sort_zip(outputs_2,
                                                   battery.connections)

                    # check if swapping the houses is possible and creates
                    # enough space (incuded offset when needed)
                    for house_1 in sorted_house_1:
                        for house_2 in sorted_house_2:
                            output_diff = house_1.output - house_2.output
                            if (output_diff - (needed_space - offset -
                                               sorted_batt[0].capacity) > 0
                                    and battery.capacity -
                                    output_diff > 0):
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

    def profitable_swap(self, index_1, index_2, temperature=1):
        """
        Checks if swapping two house-battery
        connections is possible and decreases the
        total cost.
        Swaps when favourable.
        Possibility to activate simulated annealing.
        """
        # if in archive skip
        if index_1 and index_2 in self.previous:
            return False

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
        distance_change = (dist_1 + dist_2) - (dist_1_new + dist_2_new)

        # create archive to prevent back and forward walking
        if distance_change == 0:
            self.previous.append(index_1)
            self.previous.append(index_2)
        elif distance_change > 0:
            self.previous = []

        # swap when profitable
        if distance_change >= 0:
            self.grid.swap(house_1, house_2)
            return True

        # simulated annealing
        random_number = random.random()
        if (temperature > 1 and math.exp(distance_change / temperature) >
                random_number):
            self.grid.swap(house_1, house_2)
            self.previous = []
            return True

        return False

    def random_hillclimber(self, lineplot=False, annealing=False):
        """
        Search local optimum by random profitable
        swapping.
        When lineplot = True: plot a lineplot
        """

        # variables
        temperature = [1]
        cap = len(self.grid.houses) * (len(self.grid.houses) - 1)
        swapped = 0
        plot = Plots(self.grid)
        cost_list = []
        temp_list = []
        swapped_list = []
        N = cap
        T_0 = 80
        # climb until nothing changes for 22500 iterations
        while cap > 0:
            # temperature for annealing
            if annealing:
                temperature = self.temp_function(len(swapped_list), 300, 'exp',
                                                 T_0)
                T_0 = temperature[1]
                temp_list.append(temperature[0])

            cap -= 1
            index_1 = random.randint(0, (len(self.grid.houses) - 1))
            index_2 = random.randint(0, (len(self.grid.houses) - 1))
            if self.profitable_swap(index_1, index_2, temperature[0]):
                swapped += 1
                swapped_list.append(swapped)
            cost_list.append(plot.cost())

            if len(cost_list) > 2 and cost_list[-1] == cost_list[-2]:
                continue
            else:
                cap = len(self.grid.houses) * (len(self.grid.houses) - 1)

        # plot lineplot
        if lineplot:
            plt.plot(cost_list)
            plt.ylabel("costs")
            plt.xlabel("iterations")

    def k_means(self, houses, batteries):
        """
        Apply a K-means algorithm to the grid
        """
        changes = 1
        iterations = 0
        old_connection = None
        for i in range(100):
            iterations += 1
            changes = 0
            used = []
            not_used = []

            # calculate old distances
            self.grid.distances(houses, batteries)

            # clear battery connections
            for battery in batteries:
                battery.connections = []
                battery.capacity = battery.max_cap

            for house in houses:

                sort_batteries = self.sort_zip(house.distances, batteries)
                if not house.connection == batteries.index(sort_batteries[0]):
                    changes += 1

                # select closest battery
                # check if battery capacity is sufficient
                # else select next closest battery
                count = 0
                for battery in sort_batteries:
                    count += 1
                    if (battery.capacity - house.output) > 0:
                        battery.capacity -= house.output
                        house.connect(batteries.index(battery))
                        used.append(house)
                        battery.connect(house)
                        break

                    # if no battery can fit the house, add it to unused
                    if count == len(batteries):
                        not_used.append(house)

            # reposition battery according to average xy
            for battery in batteries:
                x, y = 0, 0
                used_battloc = []

                for house in battery.connections:
                    x += house.x
                    y += house.y
                x = round(x / len(battery.connections))
                y = round(y / len(battery.connections))

                # random location + location free check
                house_on_spot = True
                while house_on_spot:
                    broken = False

                    # check if coordinates already taken
                    if [x, y] in used_battloc:
                        broken = True
                        break

                    # check if house on location
                    for house in self.grid.houses:
                        if broken:
                            break
                        if [house.x, house.y] == [x, y]:
                            house_on_spot = True
                            broken = True
                            break

                    # place battery when location free
                    if not broken:
                        house_on_spot = False
                        used_battloc.append([x, y])
                        battery.x = x
                        battery.y = y
                    else:
                        # move battery slighty
                        choices = [1, -1, 0]
                        x_step = random.choice(choices)
                        y_step = random.choice(choices)
                        x += x_step
                        y += y_step
                        if x > 50 or x < 0:
                            x -= 2 * x_step
                        elif y > 50 or y < 0:
                            y -= 2 * y_step

            # calculate new distances
            self.grid.distances(houses, batteries)

        # if not all houses connected, make space
        if len(used) < len(houses):
            for i in not_used:
                i.connection = None

            self.capacity_fixer(not_used)

    def battery_placer(self, option):
        """
        Places a given set of batteries on random locations
        """

        # empty batteries list
        self.grid.batteries = []

        # list for used coordinates batteries
        used = []

        # place batteries random on the grid for small, medium and large
        battery_kinds = ["SMALL", "MEDIUM", "LARGE"]
        for i in range(len(option)):
            used = self.place_battery_kind(option[i], battery_kinds[i], used)

        # use k means on the grid
        self.k_means(self.grid.houses, self.grid.batteries)

    def place_battery_kind(self, number, kind, used):
        """
        Place "number" times "kind" battery on
        the grid (when place not taken yet)
        """

        for i in range(number):

            # random location + location free check
            house_on_spot = True
            while house_on_spot:
                broken = False

                # the random coordinates
                x = round(random.random() * 50)
                y = round(random.random() * 50)

                # check if coordinates already taken
                if [x, y] in used:
                    broken = True
                    break

                # check if house on location
                for house in self.grid.houses:
                    if broken:
                        break
                    if [house.x, house.y] == [x, y]:
                        house_on_spot = True
                        broken = True
                        break

                # place battery when location free
                if not broken:
                    house_on_spot = False
                    used.append([x, y])

            # add to list
            self.grid.batteries.append(Battery(x, y, kind))

        return used

    def temp_function(self, i, N, type, T_0):
        """
        Calculates temperature
        Source: http://www.theprojectspot.com/tutorial-post/simulated-annealing
                -algorithm-for-beginners/6
        """

        coolRate = i/N
        T_N = 1
        if type == 'exp':
            T = T_0 ** (1-(coolRate))
        elif type == 'lin':
            T = T_0 - i * (T_0 - T_N) / N

        return [T, T_0]

    def arrr_starrr(self, house_in, battery_in):
        """
        Implement an aglorithm that avoids cables running under houses
        and lays a path around them
        """

        # cost of stepping somewhere
        cost_step = 9
        cost_house = 5000
        cost_battery = 10000

        # locations houses and batteries
        house_locations = []
        battery_locations = []
        for house in self.grid.houses:
            house_locations.append((house.x, house.y))
        for battery in self.grid.batteries:
            battery_locations.append((battery.x, battery.y))

        # start and end conditions
        x_house = house_in.x
        y_house = house_in.y
        x_battery = battery_in.x
        y_battery = battery_in.y
        start = (x_house, y_house)
        end = (x_battery, y_battery)

        # open and closed set
        open_set = {}
        closed_set = {}
        parents = {}

        # start sets
        open_set[start] = [(abs(start[1] - end[1]) +
                            abs(start[0] - end[0])) * cost_step, cost_step]

        # loop until cheapest route found
        while len(open_set) > 0:

            # take lowest f-value in open_set
            node = min(open_set, key=open_set.get)
            f_node = open_set[node][0]
            g_node = open_set[node][1]
            open_set.pop(node)
            closed_set[node] = [f_node, g_node]

            # check if found
            if node == end:
                return [self.make_path(parents, node), g_node - cost_battery]

            # create children current node
            up = (node[0], node[1] + 1)
            down = (node[0], node[1] - 1)
            left = (node[0] - 1, node[1])
            right = (node[0] + 1, node[1])
            children = [up, down, left, right]

            # iterate over children
            for child in children:

                # if already evaluated continue
                if child in closed_set:
                    continue

                # check valid location
                if child[0] < 0 or child[1] < 0:
                    continue
                if child[0] > 149 or child[1] > 149:
                    continue

                # determine g-value
                if child in house_locations:
                    g_new = g_node + cost_house
                elif child in battery_locations:
                    g_new = g_node + cost_battery
                else:
                    g_new = g_node + cost_step

                # if not visited yet, add to open set
                if child not in open_set:
                    open_set[child] = [(abs(child[1] - end[1]) +
                                        abs(child[0] - end[0])) * cost_step +
                                       g_node, g_new]
                elif g_new >= open_set[child][1]:
                    continue

                # record path
                parents[child] = node
                open_set[child][0] = g_new + (abs(child[1] - end[1]) +
                                              abs(child[0] -
                                                  end[0])) * cost_step
                open_set[child][1] = g_new

    def make_path(self, parents, node):
        """Makes path from a star results"""

        # start coordinates in path lists
        x_values = [node[0]]
        y_values = [node[1]]

        # trance the path and add coordinates to lists
        while node in parents:
            node = parents[node]
            x_values.append(node[0])
            y_values.append(node[1])

        # return path values
        return [x_values, y_values]

    def simulated_annealing(self, N):
        """
        Implements a simulated annealing algorithm to reach the global
        minimum and avoid local minima
        """
        plot = Plots(self.grid)
        best_cost = plot.cost()
        best_algo = copy.deepcopy(self)
        list_algo = []
        for i in range(N):
            self.random_hillclimber(True, True)
            list_algo.append(plot.cost())
            if plot.cost() < best_cost:
                best_cost = plot.cost()
                best_algo = copy.deepcopy(self)

        return [best_algo, list_algo]

    def possibilities_calculator(self):
        """
        A function that calculates the least amount of battery
        combinations that are possible, taking into account the capacity
        """
        # calculate the sum of all house outputs
        output = 0
        for house in self.grid.houses:
            output += house.output

        # declare the battery capacities
        # small, medium, large
        cap_kind = [450, 900, 1800]
        options = []
        max_num = [0, 0, 0]

        for i in range(len(cap_kind)):
            max_num[i] = round(output / cap_kind[i])
        i = 0
        j = 0
        k = 0
        for i in range(max_num[2] + 1):
            for j in range(max_num[1] + 1):
                for k in range(max_num[0] + 1):
                    total_cap = i * cap_kind[2] + j * cap_kind[1] + \
                                k * cap_kind[0]
                    if total_cap >= output and \
                       total_cap < (output + cap_kind[0]) and \
                       [k, j, i] not in options:
                        options.append([k, j, i])
        return options

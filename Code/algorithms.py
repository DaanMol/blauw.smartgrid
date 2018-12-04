from grid import Grid
from actions import Plots
# from bokeh import Bokeh
import matplotlib.pyplot as plt
import random
import time
import math
import copy


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
        if temperature > 1 and math.exp(distance_change / temperature) > random_number:
            self.grid.swap(house_1, house_2)
            self.previous = []
            return True
        # elif distance_change >= 0:
        #     self.grid.swap(house_1, house_2)
        #     return True
        return False

    def random_hillclimber(self, lineplot=False, annealing=False):
        """
        Search local optimum by random profitable
        swapping.
        When lineplot = True: plot a lineplot
        """

        # variables
        temperature = 1
        cap = len(self.grid.houses) * (len(self.grid.houses) - 1)
        swapped = 0
        plot = Plots(self.grid)
        cost_list = []
        swapped_list = []
        N = cap

        # climb until nothing changes for 22500 iterations
        while cap > 0:
            # temperature for annealing
            if annealing:
                temperature = self.temp_function(len(cost_list), N, 'exp')

            cap -= 1;
            index_1 = random.randint(0, (len(self.grid.houses) - 1))
            index_2 = random.randint(0, (len(self.grid.houses) - 1))
            if self.profitable_swap(index_1, index_2, temperature):
                swapped += 1
            cost_list.append(plot.cost())
                # swapped_list.append(swapped)
            if len(cost_list) > 2 and cost_list[-1] == cost_list[-2]:
                continue
            else:
                # N += 22350 - cap
                cap = len(self.grid.houses) * (len(self.grid.houses) - 1)

        # plot lineplot
        if lineplot:
            plt.plot(cost_list)
            plt.title("hillclimber: cost vs iterations")
            # plt.plot(swapped_list)

    def k_means(self, houses, batteries):
        """
        Apply a K-means algorithm to the grid
        Currently neglects the capacity of the battery
        """
        changes = 1
        iterations = 0
        old_connection = None
        print("KMEANING")
        for i in range(100):
            iterations += 1
            changes = 0
            used = []
            not_used = []

            # calculate old distances
            self.grid.distances(houses, batteries)

            # clear battery connectoins
            for battery in batteries:
                battery.connections = []
                battery.capacity = battery.max_cap

            for house in houses:

                sorted_batteries = self.sort_zip(house.distances, batteries)
                if not house.connection == batteries.index(sorted_batteries[0]):
                    changes += 1

                # select closest battery
                # check if battery capacity is sufficient
                # else select next closest battery
                count = 0
                for battery in sorted_batteries:
                    count += 1
                    if (battery.capacity - house.output) > 0:
                        battery.capacity -= house.output
                        house.connect(batteries.index(battery))
                        used.append(house)
                        battery.connect(house)
                        break

                    # if no battery can fit the house, add it to unused
                    if count == 5:
                        not_used.append(house)

            # reposition battery according to average xy
            for battery in batteries:
                x, y = 0, 0
                for house in battery.connections:
                    x += house.x
                    y += house.y
                battery.x = round(x / len(battery.connections))
                battery.y = round(y / len(battery.connections))

            # calculate new distances
            self.grid.distances(houses, batteries)

        if len(used) < len(houses):
            print('ficing cap brub')
            self.capacity_fixer(not_used)

    def splitter(self):
        """
        Splits batteries into smaller ones to possibly
        reduce the costs
        """
        print("NOW SPLITTING")
        # split every battery
        bat_count = 0
        # assign the original batteries to a variable so the program does not
        # run infinitely because the self.grid.batteries is extended
        old_bats = copy.deepcopy(self.grid.batteries)
        print(old_bats)

        # loop over the batteries in the old state (currently 1 cuz test)
        for i in range(0,5):
            print(i)
            # calculate distances
            self.grid.distances(self.grid.houses, self.grid.batteries)
            # for house in

            # calculate the old cost of the cluster to compare later
            curr_cost = old_bats[i].cost
            for house in old_bats[i].connections:
                curr_cost += house.distances[house.connection] * 9
            curr_cost += old_bats[i].cost

            print("currcost", curr_cost)

            battery = old_bats[i]
            bat_count += 1

            # create new battery objects with the new xy
            sub_bat = MedBattery(battery.x + 1, battery.y + 1)
            sub_bat2 = MedBattery(battery.x - 1, battery.y - 1)
            old_bat = battery
            # TODO give batteries the connections: split em from the original
                # this is being done in kmeans i think

            # houses is now the houses in the battery cluster
            # SUMTING RONG
            houses = battery.connections
            # batteries is now the newly created batteries
            batteries = [sub_bat, sub_bat2]
            # calculate distances for the new batteries and the houses
            # do this at the beginning of kmeans??
            # self.grid.distances(houses, batteries)

            # add the new houses to the grid batteries list
            self.grid.batteries.append(sub_bat)
            self.grid.batteries.append(sub_bat2)

            # still need to remove the old one
            # removing old one V
            self.grid.batteries.remove(self.grid.batteries[i])

            # calculate new cost but doesnt work cuz 2 new batteries
            # this function wont work either duh...


            # deepcopy the old gridstate to reverse if this doesnt save money
            old_grid = copy.deepcopy(self.grid)

            # run k-Means on the new 2 clusters
            self.k_means(houses, batteries)


            # calculate new cost
            new_cost = 0
            # for battery in self.grid.batteries:
            #     for house in battery.connections:
            #         new_cost += house.distances[house.connection] * 9
            #     new_cost += battery.cost

            # split the battery in 2 batteries one level down
            # do a k-means on them using only the first battery's population
                # this needs work since some houses are double connected
            # check if it's cheaper
            # once more for the smalles battery

    def combiner(self):
        # place 17 small batteries: enough to reach capacity
        # check if combining the two closest batteries costs less
        # if so combine, else: next battery
        # repeat untill all combinations are checked
        # move up a battery level
        # repeat untill last level is reached
        # ???
        # profit
        pass

    def temp_function(self, i, N, type):
        """
        Calculates temperature
        Source:
        """
        T_0 = 800
        T_N = 1
        if type == 'exp':
            T = T_0 * (T_N / T_0) ** (i / N)
        elif type == 'lin':
            T = T_0 - i * (T_0 - T_N) / N
        return T

    def agg_clust(self):
        """
        Bottom up clustering with a dendrogram
        """
        # create cluster dict
        clusters = {}

        # fill the dict with singleton clusters at each house xy
        counter = 1
        for house in self.grid.houses:
            clusters[counter] = [house]
            counter += 1

        # while len(clusters) > 1:
            # find closest pair of clusters
            distances = []
            for cluster in clusters:
                x1 = clusters[cluster][0].x
                y1 = clusters[cluster][0].y
                for cluster2 in clusters:
                    if cluster2 == cluster:
                        continue
                    x2 = cluster[cluster2][0].x
                    y2 = cluster[cluster2][0].y

    def arrr_starrr(self, house_in, battery_in):
        """a star"""

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
        plot = Plots(self.grid)
        best_cost = plot.cost()
        best_algo = copy.deepcopy(algo)
        list_algo = []
        for i in range(N):
            current_algo = copy.deepcopy(best_algo)
            plot = Plots(current_algo.grid)
            print(i, plot.cost())
            current_algo.random_hillclimber(True, True)
            list_algo.append(plot.cost())
            if plot.cost() < best_cost:
                best_cost = plot.cost()
                best_algo = copy.deepcopy(current_algo)
                print(f"Better : {i} {best_cost} {len(list_algo)}")

        return [best_algo, list_algo]

# run
if __name__ == "__main__":
    # create algorithm Object
    algo = Algorithm(1)

    algo.random_cap()

    final = algo.simulated_annealing(450)

    plot = Plots(final[0].grid)
    with open(f"simulated_annealing1_450.txt", 'w') as f:
            for i in final[1]:
                f.write(f"{i}\n")
    plot.x_or_y_first(False, "simulated_annealing")

    # create bokeh object
    # bokeh = Bokeh(algo.grid)
    # bokeh.simple_plot()

    """Algorithms"""
    # algo.random_cap()
    # algo.random_hillclimber()
    # plot.arrr_starrr_graph()
    # algo.proximity_first()
    # # algo.priority_first()
    # cost_1 = plot.cost()
    # print("start =", cost_1)
    #
    # algo.random_hillclimber()
    # for i in algo.grid.batteries:
    #     print(i.capacity)
    # cost_2 = plot.cost()
    # print("improvement =", cost_1 - cost_2)
    # print("end =", cost_2)

    # algo.k_means()
    # algo.house_to_bat()
<<<<<<< HEAD
    for j in range(1,4):
        cost = []
        for i in range(10000):
            algo = Algorithm(j)
            plot = Plots(algo.grid)
            algo.random_cap()
            # algo.k_means()
            # algo.priority_first()
            # print(plot.cost())
            # cost_annealing = []
            # for i in range(1000):
            #     algo.random_hillclimber(False, True)
            #     print(i/10)
            #     cost_annealing.append(plot.cost())

            algo.k_means()
            algo.random_hillclimber()
            # algo.arrr_starrr()

            # print(plot.cost())
            curr_cost = plot.cost()
            cost.append(curr_cost)
            if i%1 == 0:
                print("check", i/1)
            # for i in algo.grid.batteries:
            #     print(i.capacity)
        with open(f"text_k-means_hill{j}_10000.txt", 'w') as f:
            for i in cost:
                f.write(f"{i}\n")
    plt.figure()
    plt.hist(cost, bins=100)
    print(min(cost))
    # print(cost)
    print("min =", min(cost))
    print("max =", max(cost))
=======
    # for j in range(1,4):
    #     cost = []
    #     for i in range(1000):
    #         algo = Algorithm(j)
    #         plot = Plots(algo.grid)
    #         algo.random_cap()
    #         # algo.k_means()
    #         # algo.priority_first()
    #         # print(plot.cost())
    #         # cost_annealing = []
    #         # for i in range(1000):
    #         #     algo.random_hillclimber(False, True)
    #         #     print(i/10)
    #         #     cost_annealing.append(plot.cost())
    #
    #         algo.k_means()
    #         algo.random_hillclimber()
    #         # algo.arrr_starrr()
    #
    #         # print(plot.cost())
    #         curr_cost = plot.cost()
    #         cost.append(curr_cost)
    #         if i%1 == 0:
    #             print("check", i/1)
    #         # for i in algo.grid.batteries:
    #         #     print(i.capacity)
    #     with open(f"text_k-means_hill{j}_1000.txt", 'w') as f:
    #         for i in cost:
    #             f.write(f"{i}\n")
    # plt.figure()
    # plt.hist(cost, bins=100)
    # print(min(cost))
    # # print(cost)
    # print("min =", min(cost))
    # print("max =", max(cost))
>>>>>>> bb25c0794756b79294ee3a4b8a166a6e416d8f5f

    # algo.random_hillclimber(100000)
    # plot = Plots(list)

    """Plots"""
    # plots
    # plot.line_figure("hillclimber")
    # plot.x_or_y_first(False, "hillclimber")
    # plot.random_simulation(False, "hillclimber")

    # calculate cost
    # print("cost =", plot.cost())

    # show plots
    plt.show()

    # plot.plot_histograms_bokeh()
    # plot.plot_grid_bokeh()
    # plot.plot_matrix_bokeh()

from grid import Grid
import matplotlib.pyplot as plt
import random
import time
import numpy as np

class Algorithm():
    """
    ALGORITHMSSSS
    """
    def __init__(self, district):
        """
        something something
        """
        self.grid = Grid(district)

    def algorithm_0(self, already_used=[]):
        used = already_used
        for battery in self.grid.batteries:
            capacity = battery.capacity
            for house in self.grid.houses:
                if house not in used and capacity - house.output > 0:
                    battery.connect(house)
                    capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))
        if len(used) < 150:
            self.swapper(used)

    def algorithm_1(self, already_used=[]):
        used = already_used
        for battery in self.grid.batteries:
            capacity = battery.capacity
            distances = battery.distances
            houses = self.grid.houses
            sorted_houses = [x for (y,x) in sorted(zip(distances,houses), key=lambda pair: pair[0])]
            for house in sorted_houses:
                if house not in used and capacity - house.output > 0:
                    battery.connect(house)
                    capacity -= house.output
                    used.append(house)
                    house.connect(self.grid.batteries.index(battery))
        if len(used) < 150:
            self.swapper(used)

    def algorithm_2(self):
        used = []
        relatives = []
        for house in self.grid.houses:
            c_1 = sorted(house.distances)[1] - sorted(house.distances)[0]
            relatives.append(c_1)
        sorted_houses = [x for (y,x) in sorted(zip(relatives,self.grid.houses),
                         key=lambda pair: pair[0], reverse=True)]
        for house in sorted_houses:
            sorted_batteries = [x for (y,x) in \
                                sorted(zip(house.distances, self.grid.batteries),
                                key=lambda pair: pair[0])]

            for i in range(len(sorted_batteries)):
                batt_now = sorted_batteries[i]
                batt_next = sorted_batteries[i + 1]
                # skip when capacity is larger than the next in list
                if batt_next.capacity - batt_now.capacity > 0 and \
                   batt_next.capacity < batt_now.capacity:
                    if i < 3:
                        continue
                    else:
                        batt_now = batt_next
                # continue if capacity too small
                if batt_now.capacity - house.output < 0:
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

        if len(used) < 150:
            self.swapper(used)

    def swapper(self, used):
        print(len(used))


    def hillclimber(self, N):
        for i in range(N):
            random_index_1 = int(random.uniform(0, 149))
            random_index_2 = int(random.uniform(0, 149))
            house_1 = self.grid.houses[random_index_1]
            print(house_1)
            house_2 = self.grid.houses[random_index_2]
            if house_1 == house_2:
                continue
            battery_1 = self.grid.batteries[house_1.connection]
            battery_2 = self.grid.batteries[house_2.connection]
            if battery_1 == battery_2:
                continue
            if battery_1.capacity - house_1.output + house_2.output < 0:
                continue
            if battery_2.capacity - house_2.output + house_1.output < 0:
                continue
            distance_1_old = house_1.distances[house_1.connection]
            distance_2_old = house_2.distances[house_2.connection]
            distance_1_new = house_1.distances[house_2.connection]
            distance_2_new = house_2.distances[house_1.connection]
            if distance_1_old + distance_2_old < distance_1_new + distance_2_new:
                continue
            print("Climbing that hill!")
            battery_1.connections.remove(house_1)
            battery_2.connections.remove(house_2)
            temp = house_1.connection
            house_1.connection = house_2.connection
            house_2.connection = temp
            battery_1.capacity = battery_1.capacity - house_1.output + house_2.output
            battery_2.capacity = battery_2.capacity - house_2.output + house_1.output
            battery_1.connections.append(house_2)
            battery_1.connections.append(house_1)

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
                sorted_batteries = [x for (y,x) in sorted(zip(distances,batteries),
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
                print(battery.connections)
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
            print('------')
        print('iterations: ', iterations)

    def line_figure(self):
        plt.figure()
        counter = 0
        cost = 0
        colors = ['r', 'b', 'g', 'y', 'm']
        for battery in algo.grid.batteries:
            x = []
            y = []
            for house in battery.connections:
                cost += house.distances[house.connection] * 9
                x.append(house.x)
                y.append(house.y)
                plt.plot([house.x, battery.x], [house.y, battery.y], color=colors[counter], linewidth=.25)
            plt.scatter(x, y, marker='p', color=colors[counter])
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
            counter += 1
        print("cost =", cost)

    def random_simulation(self, simulation):
        counter = 0
        plt.figure()
        colors = ['r', 'b', 'g', 'y', 'm']
        for battery in algo.grid.batteries:
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
            x = []
            y = []
            for house in battery.connections:
                x.append(house.x)
                y.append(house.y)
            plt.scatter(x, y, marker='p', color=colors[counter])
            counter += 1

        counter = 0
        for battery in algo.grid.batteries:
            for house in battery.connections:
                curr_x, curr_y = house.x, house.y
                end_x, end_y = battery.x, battery.y
                if curr_x > end_x:
                    x_step = -1
                else:
                    x_step = 1
                if curr_y > end_y:
                    y_step = -1
                else:
                    y_step = 1
                while not curr_x == end_x and not curr_y == end_y:
                    if random.random() < 0.5:
                        plt.plot([curr_x, curr_x], [curr_y, curr_y + y_step], color=colors[counter], linewidth=.3)
                        curr_y = curr_y + y_step
                    else:
                        plt.plot([curr_x, curr_x + x_step], [curr_y, curr_y], color=colors[counter], linewidth=.3)
                        curr_x = curr_x + x_step
                plt.plot([curr_x, end_x], [curr_y, end_y], color=colors[counter], linewidth=.3)
            counter += 1
            if simulation:
                plt.pause(1)
                plt.draw()

    def x_or_y_first(self, x_first):
        plt.figure()
        if x_first:
            counter = 0
            colors = ['r', 'b', 'g', 'y', 'm']
            for battery in algo.grid.batteries:
                x = []
                y = []
                for house in battery.connections:
                    x.append(house.x)
                    y.append(house.y)
                    plt.plot([house.x, battery.x], [house.y, house.y], color=colors[counter], linewidth=.3)
                    plt.plot([battery.x, battery.x], [house.y, battery.y], color=colors[counter], linewidth=.3)
                plt.scatter(x, y, marker='p', color=colors[counter])
                plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
                counter += 1
        else:
            counter = 0
            colors = ['r', 'b', 'g', 'y', 'm']
            for battery in algo.grid.batteries:
                x = []
                y = []
                for house in battery.connections:
                    x.append(house.x)
                    y.append(house.y)
                    plt.plot([house.x, house.x], [house.y, battery.y], color=colors[counter], linewidth=.3)
                    plt.plot([house.x, battery.x], [battery.y, battery.y], color=colors[counter], linewidth=.3)
                plt.scatter(x, y, marker='p', color=colors[counter])
                plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
                counter += 1

# run
if __name__ == "__main__":
    algo = Algorithm(1)

    """
    Algorithms
    """
    # algo.algorithm_0()
    # algo.algorithm_1()
    algo.algorithm_2()
    # algo.hillclimber(100)
    # algo.k_means()

    """
    Plots
    """
    # algo.random_simulation(False)
    algo.x_or_y_first(False)
    # algo.line_figure(self)

    plt.show()

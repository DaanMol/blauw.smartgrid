from grid import Grid
import matplotlib.pyplot as plt
import random
import time

class Algorithm():
    """
    ALGORITHMSSSS
    """
    def __init__(self, district):
        """
        something something
        """
        self.grid = Grid(district)

    def algorithm_0(self):
        used = []
        for battery in self.grid.batteries:
            capacity = battery.capacity
            connections = []
            for house in self.grid.houses:
                if house not in used and capacity - house.output > 0:
                    connections.append(house)
                    capacity -= house.output
                    used.append(house)
                    house.connection = self.grid.batteries.index(battery)
            battery.connections = connections
            battery.capacity = capacity

    def algorithm_1(self):
        used = []
        for battery in self.grid.batteries:
            capacity = battery.capacity
            connections = []
            distances = battery.distances
            houses = self.grid.houses
            sorted_houses = [x for (y,x) in sorted(zip(distances,houses), key=lambda pair: pair[0])]
            for house in sorted_houses:
                if house not in used and capacity - house.output > 0:
                    connections.append(house)
                    capacity -= house.output
                    used.append(house)
                    house.connection = self.grid.batteries.index(battery)
            battery.connections = connections
            battery.capacity = capacity

# run
if __name__ == "__main__":
    algo = Algorithm(1)

    algo.algorithm_1()

    # plt.figure("algorithm_0")
    # counter = 0
    # cost = 0
    # colors = ['r', 'b', 'g', 'y', 'm']
    # for battery in algo.grid.batteries:
    #     x = []
    #     y = []
    #     for house in battery.connections:
    #         cost += house.distances[house.connection] * 9
    #         x.append(house.x)
    #         y.append(house.y)
    #         plt.plot([house.x, battery.x], [house.y, battery.y], color=colors[counter], linewidth=.25)
    #     plt.scatter(x, y, marker='p', color=colors[counter])
    #     plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
    #     counter += 1
    # print("cost =", cost)
    #
    # plt.figure("tryout_xfirst")
    # counter = 0
    # colors = ['r', 'b', 'g', 'y', 'm']
    # for battery in algo.grid.batteries:
    #     x = []
    #     y = []
    #     for house in battery.connections:
    #         x.append(house.x)
    #         y.append(house.y)
    #         plt.plot([house.x, battery.x], [house.y, house.y], color=colors[counter], linewidth=.3)
    #         plt.plot([battery.x, battery.x], [house.y, battery.y], color=colors[counter], linewidth=.3)
    #     plt.scatter(x, y, marker='p', color=colors[counter])
    #     plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
    #     counter += 1
    #
    # plt.figure("tryout_yfirst")
    # counter = 0
    # colors = ['r', 'b', 'g', 'y', 'm']
    # for battery in algo.grid.batteries:
    #     x = []
    #     y = []
    #     for house in battery.connections:
    #         x.append(house.x)
    #         y.append(house.y)
    #         plt.plot([house.x, house.x], [house.y, battery.y], color=colors[counter], linewidth=.3)
    #         plt.plot([house.x, battery.x], [battery.y, battery.y], color=colors[counter], linewidth=.3)
    #     plt.scatter(x, y, marker='p', color=colors[counter])
    #     plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
    #     counter += 1
    counter = 0
    plt.figure("tryout_random")
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
        plt.pause(1)
        plt.draw()
plt.show()

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

    def algorithm_0(self, already_used=[]):
        used = already_used
        for battery in self.grid.batteries:
            capacity = battery.capacity
            connections = battery.connections
            for house in self.grid.houses:
                if house not in used and capacity - house.output > 0:
                    connections.append(house)
                    capacity -= house.output
                    used.append(house)
                    house.connection = self.grid.batteries.index(battery)
        if len(used) < 150:
            self.swapper(used)

    def algorithm_1(self, already_used=[]):
        used = already_used
        for battery in self.grid.batteries:
            capacity = battery.capacity
            connections = battery.connections
            distances = battery.distances
            houses = self.grid.houses
            sorted_houses = [x for (y,x) in sorted(zip(distances,houses), key=lambda pair: pair[0])]
            for house in sorted_houses:
                if house not in used and capacity - house.output > 0:
                    connections.append(house)
                    capacity -= house.output
                    used.append(house)
                    house.connection = self.grid.batteries.index(battery)
        if len(used) < 150:
            self.swapper(used)

    def algorithm_2(self):
        used = []
        relatives = []
        for i in self.grid.houses:
            c_1 = sorted(i.distances)[1] - sorted(i.distances)[0]
            relatives.append(c_1)
        sorted_houses = [x for (y,x) in sorted(zip(relatives,self.grid.houses), key=lambda pair: pair[0], reverse=True)]
        for i, k in zip(sorted_houses, sorted(relatives, reverse=True)):
            sorted_batteries = [x for (y,x) in sorted(zip(i.distances,self.grid.batteries), key=lambda pair: pair[0])]
            for j in sorted_batteries:
                if j.capacity - i.output > 0:
                    j.capacity = j.capacity - i.output
                    j.connections.append(i)
                    i.connection = self.grid.batteries.index(j)
                    used.append(i)
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



# run
if __name__ == "__main__":
    for i in range(3):
        algo = Algorithm(i+1)

        algo.algorithm_0()
        algo.algorithm_1()
        algo.algorithm_2()
    # algo.hillclimber(100)

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

    # counter = 0
    # plt.figure("tryout_random")
    # colors = ['r', 'b', 'g', 'y', 'm']
    # for battery in algo.grid.batteries:
    #     plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
    #     x = []
    #     y = []
    #     for house in battery.connections:
    #         x.append(house.x)
    #         y.append(house.y)
    #     plt.scatter(x, y, marker='p', color=colors[counter])
    #     counter += 1
    #
    # counter = 0
    # for battery in algo.grid.batteries:
    #     for house in battery.connections:
    #         curr_x, curr_y = house.x, house.y
    #         end_x, end_y = battery.x, battery.y
    #         if curr_x > end_x:
    #             x_step = -1
    #         else:
    #             x_step = 1
    #         if curr_y > end_y:
    #             y_step = -1
    #         else:
    #             y_step = 1
    #         while not curr_x == end_x and not curr_y == end_y:
    #             if random.random() < 0.5:
    #                 plt.plot([curr_x, curr_x], [curr_y, curr_y + y_step], color=colors[counter], linewidth=.3)
    #                 curr_y = curr_y + y_step
    #             else:
    #                 plt.plot([curr_x, curr_x + x_step], [curr_y, curr_y], color=colors[counter], linewidth=.3)
    #                 curr_x = curr_x + x_step
    #         plt.plot([curr_x, end_x], [curr_y, end_y], color=colors[counter], linewidth=.3)
    #     counter += 1
    #     plt.pause(1)
    #     plt.draw()
# plt.show()

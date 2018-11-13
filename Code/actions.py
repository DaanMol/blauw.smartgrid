import matplotlib.pyplot as plt
import random
import time


class Plots():

    def __init__(self, grid):
        self.grid = grid

    def line_figure(self):
        plt.figure()
        counter = 0
        colors = ['r', 'b', 'g', 'y', 'm']
        for battery in self.grid.batteries:
            x = []
            y = []
            for house in battery.connections:
                x.append(house.x)
                y.append(house.y)
                plt.plot([house.x, battery.x], [house.y, battery.y],
                         color=colors[counter], linewidth=.25)
            plt.scatter(x, y, marker='p', color=colors[counter])
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
            counter += 1

    def random_simulation(self, simulation):
        counter = 0
        plt.figure()
        colors = ['r', 'b', 'g', 'y', 'm']
        for battery in self.grid.batteries:
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
            x = []
            y = []
            for house in battery.connections:
                x.append(house.x)
                y.append(house.y)
            plt.scatter(x, y, marker='p', color=colors[counter])
            counter += 1

        counter = 0
        for battery in self.grid.batteries:
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
                        plt.plot([curr_x, curr_x], [curr_y, curr_y + y_step],
                                 color=colors[counter], linewidth=.3)
                        curr_y = curr_y + y_step
                    else:
                        plt.plot([curr_x, curr_x + x_step], [curr_y, curr_y],
                                 color=colors[counter], linewidth=.3)
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
            for battery in self.grid.batteries:
                x = []
                y = []
                for house in battery.connections:
                    x.append(house.x)
                    y.append(house.y)
                    plt.plot([house.x, battery.x], [house.y, house.y],
                             color=colors[counter], linewidth=.3)
                    plt.plot([battery.x, battery.x], [house.y, battery.y],
                             color=colors[counter], linewidth=.3)
                plt.scatter(x, y, marker='p', color=colors[counter])
                plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
                counter += 1
        else:
            counter = 0
            colors = ['r', 'b', 'g', 'y', 'm']
            for battery in self.grid.batteries:
                x = []
                y = []
                for house in battery.connections:
                    x.append(house.x)
                    y.append(house.y)
                    plt.plot([house.x, house.x], [house.y, battery.y],
                             color=colors[counter], linewidth=.3)
                    plt.plot([house.x, battery.x], [battery.y, battery.y],
                             color=colors[counter], linewidth=.3)
                plt.scatter(x, y, marker='p', color=colors[counter])
                plt.plot(battery.x, battery.y, marker='x', color=colors[counter], markersize=10)
                counter += 1

    def cost(self):
        cost = 0
        for battery in self.grid.batteries:
            for house in battery.connections:
                cost += house.distances[house.connection] * 9
        return cost

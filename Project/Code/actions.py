import matplotlib.pyplot as plt
import random
import time
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Legend
from grid import Grid

colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
          '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
          '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
          '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
          '#000000']

class Plots():

    def __init__(self, grid):
        self.grid = grid

    def line_figure(self, title):
        """
        Plots houses and batteries in the grid connected through
        eucledian distance
        """

        plt.figure()
        counter = 0

        # plot the x and y for each house and battery
        for battery in self.grid.batteries:
            x = []
            y = []
            for house in battery.connections:
                x.append(house.x)
                y.append(house.y)
                plt.plot([house.x, battery.x], [house.y, battery.y],
                         color=colors[counter], linewidth=.25)
            plt.scatter(x, y, marker='p', color=colors[counter])
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter],
                     markersize=10)
            counter += 1
        plt.title(f"{title} algorithm. Cost: {self.cost()}")

    def random_simulation(self, simulation, title):
        """
        Plots current configuration of the random grid
        Connects a random path
        """

        counter = 0
        plt.figure()

        # plot each battery
        for battery in self.grid.batteries:
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter],
                     markersize=10)
            x = []
            y = []
            for house in battery.connections:
                x.append(house.x)
                y.append(house.y)
            plt.scatter(x, y, marker='p', color=colors[counter])
            counter += 1

        # plot the connection
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
                plt.plot([curr_x, end_x], [curr_y, end_y],
                         color=colors[counter], linewidth=.3)
            counter += 1

            # display the process in an animation
            if simulation:
                plt.pause(1)
                plt.draw()

    def x_or_y_first(self, x_first, title):
        """
        Plot of connections with either the x coordinate
        going down until it reaches the y coordinate, after
        which the straigth line continues to its destination,
        or straight line goes over the y coordinate and continues
        to the destination following a straight line on the x coordinate
        """

        plt.figure()
        if x_first:
            counter = 0

            # draw each dot and connection
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
                plt.plot(battery.x, battery.y, marker='x',
                         color=colors[counter], markersize=10)
                counter += 1

        # draw each dot and connection
        else:
            counter = 0
            for battery in self.grid.batteries:
                col = colors[counter]
                x = []
                y = []
                for house in battery.connections:
                    x.append(house.x)
                    y.append(house.y)
                    plt.plot([house.x, house.x], [house.y, battery.y],
                             color=col, linewidth=.3)
                    plt.plot([house.x, battery.x], [battery.y, battery.y],
                             color=col, linewidth=.3)
                plt.scatter(x, y, marker='p', color=col)
                plt.plot(battery.x, battery.y, marker='x', color=col,
                         markersize=10)
                counter += 1
        plt.title(f"{title} algorithm. Cost: {self.cost()}")

    def cost(self):
        """
        Calcualte the cost for the current grid
        """
        cost = 0
        for battery in self.grid.batteries:
            for house in battery.connections:
                cost += house.distances[house.connection] * 9
            cost += battery.cost
        return cost

    def arrr_starrr_graph(self):
        """
        Plots grid for A* algorithm
        """

        plt.figure()
        total_cost = 0

        # plot batteries
        counter = 0
        for batt in self.grid.batteries:
            plt.plot(batt.x, batt.y, marker='x',
                     color=colors[counter], markersize=10)
            counter += 1

        # iterate over houses and path
        for house in self.grid.houses:
            battery = self.grid.batteries[house.connection]

            # get path coordinates
            path_data = house.path

            # plot path and house
            plt.plot(path_data[0][0], path_data[0][1],
                     color=colors[house.connection], linewidth=.3)
            plt.plot(house.x, house.y, marker='p',
                     color=colors[house.connection])
            total_cost += path_data[1]
            plt.draw()
            plt.pause(0.000000001)

        plt.title(f"total cost = {total_cost}")

    def bench_plotter():
        """
        Plots benchmark histogram of all algorithms
        """

        # plot random as histogram, upper en lower bound as a red line
        minima = []
        for i in range(1, 4):
            cost_list = []
            with open(f"../output_runs/text_info_random{i}_10k.txt", "r") as f:
                text = f.read().split('\n')
                counter = 0
                for number in text:
                    counter += 1
                    if number is not "":
                        cost_list.append(int(number))
                    if counter == 1000:
                        break
            minim = min(cost_list)
            minima.append(minim)
            maxim = max(cost_list)
            print("random:", minim, maxim)
            plt.axvline(x=53188, color='r')
            plt.axvline(x=103030, color="r")
            plt.hist(cost_list, bins=20, alpha=0.5, label=f"Random walk")

            # plot histogram of priority and hillclimber
            cost_list = []
            with open(f"../output_runs/text_info_prior_hill{i}_\
                      1k.txt", "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))
            minim = min(cost_list)
            minima.append(minim)
            maxim = max(cost_list)
            print("prior hill:", minim, maxim)
            plt.hist(cost_list, bins=20, alpha=0.5, label=f"Priority + Hill")

            # plot histogram of simulated annealing
            cost_list = []
            with open(f"../output_runs/simulated_annealing{i}_1000.txt",
                      "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))
            minim = min(cost_list)
            minima.append(minim)
            maxim = max(cost_list)
            print("random+anneal:", minim, maxim)
            plt.hist(cost_list, bins=20, alpha=0.5,
                     label=f"Random + sim anneal")

            # plot histogram of random plus hillclimber
            cost_list = []
            with open(f"../output_runs/random_hill{i}_1000.txt", "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))
            minim = min(cost_list)
            minima.append(minim)
            maxim = max(cost_list)
            print("random+hill:", minim, maxim)
            plt.hist(cost_list, bins=100, alpha=0.5,
                     label=f"Random + Hillclimber")

            # plot histogram of kmeans plus hillclimber
            cost_list = []
            with open(f"../output_runs/text_k-means_hill{i}_\
                      1000.txt", "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))
            plt.hist(cost_list, bins=20, alpha=0.5,
                     label=f"Kmean and hill {i}")
        totalmin = min(minima)
        plt.axvline(x=totalmin, color="g")
        plt.title(f"4 algorithms Wijk {i}, lowest cost: {totalmin}")
        plt.xlabel("Cost")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')
        plt.show()

    def comb_plotter(options, num):
        """
        Plots the minimum and average cost
        of every combination of batteries for a single grid
        """

        # set variables
        average = []
        minimum = []
        opt = []

        # iterate over all possible combinations
        for j in range(25):
            i = options[j]
            cost_list = []
            with open(f"../output_runs/batt_conf_400_{num}/batt_conf_{num}_\
                      [{i[0]}_{i[1]}_{i[2]}]_400.txt", "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))

            # append values to lists for plotcoordinates
            minimum.append(min(cost_list))
            average.append(sum(cost_list)/len(cost_list))
            opt.append(f"[{i[0]}_{i[1]}_{i[2]}]")

            plt.scatter(min(cost_list), sum(cost_list)/len(cost_list),
                        label=f"[{i[0]}_{i[1]}_{i[2]}]")
            plt.text(min(cost_list) + 10, sum(cost_list) /
                     len(cost_list) - 40, f"{i}")

        # set graph properties
        plt.suptitle(f"400x randompositioning+k-means+hill for all possible \
                     battery configurations (grid {num})")
        plt.title("notation: [small, medium, large] (number of batteries)")
        plt.xlabel("min cost")
        plt.ylabel("average cost")

        plt.show()

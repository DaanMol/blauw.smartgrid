import matplotlib.pyplot as plt
import random
import time
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Legend
from grid import Grid
from actions import Plots


class Plots():

    def __init__(self, grid):
        self.grid = grid

    def line_figure(self, title):
        """
        Plots display of improvements in cost
        """

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
            plt.plot(battery.x, battery.y, marker='x', color=colors[counter],
                     markersize=10)
            counter += 1
        plt.title(f"{title} algorithm. Cost: {self.cost()}")

    def random_simulation(self, simulation, title):
        """
        Plots current configuration of the random grid
        """

        counter = 0
        plt.figure()
        colors = ['r', 'b', 'g', 'y', 'm']
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
                plt.plot(battery.x, battery.y, marker='x',
                         color=colors[counter], markersize=10)
                counter += 1
        else:
            counter = 0
            colors = ['r', 'b', 'g', 'y', 'm']
            for battery in self.grid.batteries:
                c = list(np.random.choice(range(256), size=3))
                col = random.choice(colors)
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

    def plot_histograms_bokeh(self):
        """
        Plot histograms using Bokeh
        """

        # histogram house output distribution
        list = []
        for house in self.grid.houses:
            list.append(house.output)

        hist, edges = np.histogram(list, bins=30)

        # output to static HTML file
        output_file("Graphs/Bokeh/histograms.html")

        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

        p = figure(title="House output distribution", tools=TOOLS,
                   background_fill_color="#fafafa", toolbar_location="below")
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
               fill_color="navy", line_color="blue", alpha=1)

        p.y_range.start = 0
        p.legend.location = "center_right"
        p.legend.background_fill_color = "#fefefe"
        p.xaxis.axis_label = "output house"
        p.yaxis.axis_label = "number of houses"
        p.grid.grid_line_color = "white"

        show(p)

    def plot_grid_bokeh(self):
        """
        Make a picture of the Grid using Bokeh
        """

        # output to static HTML file
        output_file("Graphs/Bokeh/layout_grid.html")

        # add houses to image
        x_h = []
        y_h = []
        for house in self.grid.houses:
            x_h.append(house.x)
            y_h.append(house.y)

        # add batteries to image
        x = []
        y = []
        for battery in self.grid.batteries:
            x.append(battery.x)
            y.append(battery.y)

        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

        p = figure(title=(f"Grid: houses and batteries"),
                   tools=TOOLS, background_fill_color="#fafafa",
                   toolbar_location="right")
        r0 = p.circle(x, y, color='red', size=10)
        r1 = p.square(x_h, y_h, color='blue')

        legend = Legend(items=[
                        ('Battery', [r0]),
                        ('House', [r1]),
                        ],)

        p.add_layout(legend, 'below')
        p.legend.click_policy = "hide"
        p.xaxis.axis_label = 'x position'
        p.yaxis.axis_label = 'y position'

        # show the results
        show(p)

    def plot_matrix_bokeh(self):
        """
        Plot matrixes using Bokeh
        """

        # output to static HTML file
        output_file("Graphs/Bokeh/matrixes.html")

        TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,\
                 zoom_out,box_zoom,undo,redo, reset,tap,save,\
                 box_select,poly_select,lasso_select"

        colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r,
                  g in zip(50+2*x, 30+2*y)]

        p = figure(title=(f"Grid: house output and batteries (red)"),
                   tools=TOOLS, toolbar_location="right")

        matrix_house = np.zeros([51, 51])
        matrix_battery = np.zeros([51, 51])
        for i in self.grid.houses:
            matrix_house[i[1]][i[0]] = i[2]
        for i in self.grid.batteries:
            p.scatter(i[0], i[1], fill_color=colors, fill_alpha=0.6,
                      line_color=None)

        p.xaxis.axis_label = 'x position'
        p.yaxis.axis_label = 'y position'

    def cost(self):
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
        colors = ['r', 'b', 'g', 'y', 'm']
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

    def random_plt(self, options):
        """
        plots configuration battery scatterplot
        """
        average = []
        minimum = []
        opt = []
        for j in range(25):
            i = options[j]
            cost_list = []
            with open(f"output_runs/batt_conf_400_1/batt_conf_1_\
                      [{i[0]}_{i[1]}_{i[2]}]_400.txt", "r") as f:
                text = f.read().split('\n')
                for number in text:
                    if number is not "":
                        cost_list.append(int(number))

            minimum.append(min(cost_list))
            average.append(sum(cost_list)/len(cost_list))
            opt.append(f"[{i[0]}_{i[1]}_{i[2]}]")

            plt.scatter(min(cost_list), sum(cost_list)/len(cost_list),
                        label=f"[{i[0]}_{i[1]}_{i[2]}]")
            plt.text(min(cost_list) + 10, sum(cost_list) /
                     len(cost_list) - 40, f"{i}")
        plt.suptitle("400x randompositioning+k-means+hill for all\
                     possible battery configurations")
        plt.title("notation: [small, medium, large] (number of batteries)")
        plt.xlabel("min cost")
        plt.ylabel("average cost")
        plt.xlim(22400, 24000)
        plt.ylim(23000, 25000)

    def bench_plotter():
        """
        Plots benchmark histogram of all algorithms
        """

        # plot random as histogram, upper en lower bound as a red line
        minima = []
        for i in range(1, 2):
            cost_list = []
            with open(f"output_runs/text_info_random{i}_10k.txt", "r") as f:
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
            with open(f"output_runs/text_info_prior_hill{i}_1k.txt", "r") as f:
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
            with open(f"output_runs/simulated_annealing{i}_1000.txt",
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
            with open(f"output_runs/random_hill{i}_1000.txt", "r") as f:
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
            with open(f"output_runs/text_k-means_hill{i}_1000.txt", "r") as f:
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

    def comb_plotter():
        """
        Plots the minimum and average cost
        of every combination of batteries
        """

        # set variables
        options = [[17, 0, 0], [15, 1, 0], [13, 2, 0], [11, 3, 0], [9, 4, 0],
                   [7, 5, 0], [5, 6, 0], [3, 7, 0], [1, 8, 0], [13, 0, 1],
                   [11, 1, 1], [9, 2, 1], [7, 3, 1], [5, 4, 1], [3, 5, 1],
                   [1, 6, 1], [9, 0, 2], [7, 1, 2], [5, 2, 2], [3, 3, 2],
                   [1, 4, 2], [5, 0, 3], [3, 1, 3], [1, 2, 3], [1, 0, 4]]
        average = []
        minimum = []
        opt = []
        num = 2

        # iterate over all possible combinations
        for j in range(25):
            i = options[j]
            cost_list = []
            with open(f"output_runs/batt_conf_400_{num}/batt_conf_{num}_\
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
        plt.suptitle(f"400x randompositioning+k-means+hill for all possible \
                     battery configurations (grid {num})")
        plt.title("notation: [small, medium, large] (number of batteries)")
        plt.xlabel("min cost")
        plt.ylabel("average cost")

        plt.show()

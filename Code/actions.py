import matplotlib.pyplot as plt
import random
import time
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Legend
from grid import Grid


class Plots():

    def __init__(self, grid):
        self.grid = grid

    def line_figure(self, title):
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
        plt.title(f"{title} algorithm. Cost: {self.cost()}")

    def random_simulation(self, simulation, title):
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

    def x_or_y_first(self, x_first, title):
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
                plt.plot(battery.x, battery.y, marker='x', color=col, markersize=10)
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
                   tools=TOOLS, background_fill_color="#fafafa", toolbar_location="right")
        r0 = p.circle(x,y, color='red', size=10)
        r1 = p.square(x_h,y_h, color='blue')

        legend = Legend(items=[
                        ('Battery', [r0]),
                        ('House', [r1]),
                        ],)

        p.add_layout(legend, 'below')
        p.legend.click_policy="hide"
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

        TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,\
                 reset,tap,save,box_select,poly_select,lasso_select"

        colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)]

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

    def random_plt(self):
        for i in range(1,4):
            cost_list = []
            with open(f"text_info_random{i}_10k.txt", "r") as f:
                # text = f.read()
                # cost_list.append(text)
                text = f.read().split('\n')
                for number in text:

                    # number = number.replace(' ', '')
                    # number = number.replace('\n', '')
                    # number = number.replace('[', '')
                    # number = number.replace(']', '')
                    if number is not "":
                        cost_list.append(int(number))
                    # print(number, type(number))
            # bins = np.linspace(min(cost_list), max(cost_list))
            plt.hist(cost_list, bins=30, alpha=0.5, label=f"Random Wijk {i}")


            cost_list = []
            with open(f"text_info_prior_hill{i}_1k.txt", "r") as f:
                # text = f.read()
                # cost_list.append(text)
                text = f.read().split('\n')
                for number in text:

                    # number = number.replace(' ', '')
                    # number = number.replace('\n', '')
                    # number = number.replace('[', '')
                    # number = number.replace(']', '')
                    if number is not "":
                        cost_list.append(int(number))
                    # print(number, type(number))
            # bins = np.linspace(min(cost_list), max(cost_list))
            plt.hist(cost_list, bins=5, alpha=1, label=f"Hill Wijk {i}")

        # plt.title("10k Random walk and 1k prior and hill")
        # plt.xlabel("Cost")
        # plt.ylabel("Frequency")
        # plt.legend(loc='upper right')
        # plt.show()

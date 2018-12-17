import matplotlib.pyplot as plt
from algorithms import Algorithm
from actions import Plots
from grid import Grid
from batteries import Battery

"""
USER GUIDE

In main, enter the settings to run an algorithm
Regarding user friendliness, the explanation of the settings is put in the
docstring of the main.

"""


# run the random algorhithm
def random():
    algo.random_cap()


def proximity_first():
    algo.proximity_first()


def priority_first():
    algo.priority_first()


def hillclimber(lineplot):
    if lineplot:
        plt.figure()
        plt.title(f"District {i}")
    algo.random_hillclimber(lineplot)


def simulated_annealing(lineplot, i):
    if lineplot:
        plt.figure()
        plt.title(f"District {i}")
    algo.random_hillclimber(lineplot, annealing=True)


def k_means():
    algo.k_means(algo.grid.houses, algo.grid.batteries)


def battery_placer(options):
    algo.battery_placer(options)


def A_star():
    for house in algo.grid.houses:
        house.path = algo.arrr_starrr(house,
                                      algo.grid.batteries[house.connection])
    plot.arrr_starrr_graph()


if __name__ == '__main__':
    """
    FILL IN VARIABLES:

    To use the special conditions: fill in within the main functions

    districts:
        List with 1, 2 and/or 3 (districts 1 2 and 3)

    Start condition (when using Algorithms(1, 2 and 3)):
        1: Random
        2: Priority
        3: Proximity

    Iterative Algorithm:
        0: To just generate a starting condition
        1: Hillclimber
            special conidtions: lineplot=True
        2: Simulated annealing
            special conditions: lineplot=True
        3: K-means
        4: Battery placer
            special condition: option
            Format: [#small batteries, #medium batteries, #large batteries]

    Additional algorithm:
        1: Hillclimber
            special conidtions: lineplot=True
        2: Simulated annealing
            special conditions: lineplot=True
        3: A Star

    Plotter:
        1: X or Y first (manhattan)
            special condition: x_first = True or False
        2: Straight lines (euclidian)
        3: Random paths (manhattan)

    Setting:
        For the original batteries (step a-c): "standard"
        For the new battery types (step d-e): "advanced"
    """

    # SET SETTINGS
    districts = [1, 2, 3]
    start_condition = 1
    iterative_algorithm = 0
    additional_algorithm = 0
    plotter = 1
    setting = "standard"

    # special conditions
    lineplot = False
    option = [1, 0, 4]
    x_first = False

    # the code below enables user friendliness and is not to be changed
    for i in districts:
        title = f'District {i}: '
        algo = Algorithm(i, setting)
        plot = Plots(algo.grid)

        # start conditions
        if iterative_algorithm in [0, 1, 2]:
            if start_condition == 0:
                print("please fill in a start condition")
                break
            elif start_condition == 1:
                random()
                title += 'Random connection'
            elif start_condition == 2:
                priority_first()
                title += 'Priority first'
            elif start_condition == 3:
                proximity_first()
                title += 'Proximity first'
            else:
                print("please fill in a proper start condition")
                break

            if iterative_algorithm == 1:
                hillclimber(lineplot)
                title += ' + hillclimber'
            elif iterative_algorithm == 2:
                simulated_annealing(lineplot, i)
                title += ' + simulated annealing'

        elif iterative_algorithm == 3:
            k_means()
            title += 'K means'
        elif iterative_algorithm == 4:
            battery_placer(option)
            title += f'Battery placer {option}'
        else:
            print("please fill in a proper algorithm number")
            break

        if additional_algorithm == 1:
            hillclimber(lineplot)
            title += ' + hillclimber'
        elif additional_algorithm == 2:
            simulated_annealing(lineplot)
            title += ' + simulated annealing'

        if additional_algorithm is not 3:
            if plotter == 0:
                print("no plot input")
            elif plotter == 1:
                plot.x_or_y_first(x_first, title)
            elif plotter == 2:
                plot.line_figure(title)
            elif plotter == 3:
                plot.random_simulation(title)

    plt.show()

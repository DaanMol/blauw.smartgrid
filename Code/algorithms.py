from grid import Grid
import matplotlib.pyplot as plt


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

# run
if __name__ == "__main__":
    algo = Algorithm(1)
    
    algo.algorithm_0()

    plt.figure("algorithm_0")
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
    plt.show()

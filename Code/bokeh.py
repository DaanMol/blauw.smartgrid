from grid import Grid
from bokeh.plotting import figure
from bokeh.io import show, output_notebook

class Bokeh():
    """
    Class containing bokeh plot
    """

    def __init__(self, grid):
        self.grid = grid


    def simple_plot(self):
        x = []
        y = []
        for house in self.grid.houses:
            x.append(house.x)
            y.append(house.y)

        p = figure(plot_width = 50, plot_height = 50, title = 'Grid')
        p.circle(x, y, size=2, color='red')

        output_notebook()
        show(p)

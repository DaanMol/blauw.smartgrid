# blauw.smartgrid
Smart grid project van groep blauw: Thomas Reus, Daan Molleman en Harmke Vliek

# Description
The git is separated into two folders. The first one is code, in which our code resides. The second one is presentation. This map contains images, powerpoints and the UML diagram that represents the data structure of the code.

# Project
The smart grid project exists of 150 houses and 5 batteries, anchored in a grid. The first phase of the project dictates a fixed location for both the houses and the batteries. All houses are in possession of some sort of green energy generator such as solar panels or windmills. The generators generate energy which has to be preserved in case the generated energy is not consumed immediately. This remaining energy is stored in one of the batteries using cable connections. The cables connecting the houses to the batteries and vice versa are constituted based on Manhattan distance, which means they cannot be set diagonally in the grid. The capacity of all batteries is limited. The first purpose of this project is connecting all the houses to the available batteries without exceeding the capacity of each battery. The second object is optimization of cable positioning which leads to the minimum amount of cable length needed to connect all houses and batteries. The third goal of this project is the minimalization of the cable length combined with the possibility of the installation of extra batteries and discover what is more beneficial; installing more batteries or developing an extensive cable network.

# Complexity
The Smart Grid problem is a complex one. To be able to calculate the state space of this problem, one needs a complexity function. The function for this specific problem is as follows: C = 𝐵^𝐻. C is complexity, b is the amount of houses and h is the amount of houses represented in the plot. The complexity for the three given grids is similar; 5^150 = 7,01 E104. Once the third goal is reached, it is possible to add extra batteries. This means that the state space will increase, as the value of variable B will be increased.

The upper and lower bounds of this case are defined in the amount of cost of the network. The upper and lower bound per grid are calculated including the fixed costs of the battery in the first two goals. These are rendered below.

![Upper and lower bound of the three grids](/Presentation/Images/bounds.png)

# Code
**Constructive algorithms**

*Random*

The random algorithm connects houses to batteries at random. This gives a representation of possible solutions for the problem. The graph has been run 10.000 times. The goal is to create algorithms that better the optimal outcome of this random walk.

![Random plot](/Presentation/Images/histo_random.png)

*Greedy*

A greedy algorithm is an algorithmic strategy that makes the optimal choice at each small stage with the goal of this eventually leading to a global optimum. This means that the algorithm picks the best immediate output without taking future outputs into consideration. The algorithm is separated into two modes; proximity first and priority first.

*Proximity first*

The proximity first algorithm connects houses to batteries based on the distance of the house to the battery. Houses who are closest are connected before houses that are farther away.

![Proximity first plot](/Presentation/Images/tryout_yfirst_alg0.png)

*Priority first*

The priority first algorithm connects houses to batteries based on the output of the houses. Houses whose output is high are connected before houses whose output is lower. The output differentiates from 20 to 70.

![Priority first plot](/Presentation/Images/tryout_yfirst.png)

**Iterative algorithms**

*Hillclimber*

A hillclimber is an algorithm that tries to find a sufficiently good solution to the problem. This solution may be a local optimal maximum instead of the global optimal maximum. The code accepts similar or better situations than the previous. If the proposed situation is not similar to or better than the last; the situation will be discarded. This will continue as long as no more than 10.000 situations are better or similar to the previous circumstances, to ensure a local maximum is reached. This situation will be rendered as the solution.

Shown below is an plot that represents ten runs of the hillclimber. It renders the relative quality of the solutions in regard to each other.

![Hillclimber relative quality](/Presentation/Images/hillclimberx10.png)

*Simulated annealing*

Simulated annealing is a algorithm in which worse solutions are accepted in order to escape a local maximum. This algorithm is not yet ready. It is however a continuation of the process rendered when the hillclimber algorithm runs, as it tries to escape the local maxima the hillclimber can enter.

*K-means*

This is an algorithm that is useful just for the third goal of this project. The K-means algorithm is a cluster algorithm. It calculates the average of all the points in a cluster and moves the centroid to that average location. This continues until there is no more change in the clusters.

Shown below is an plot that represents ten runs of the K-means. It renders the relative quality of the solutions in regard to each other.

![K-means algorithm relative quality](/Presentation/Images/kmeansx10.png)


The images shown above are created using matplotlib.pylot and Bokeh.

# Packages installed
To run the code, several packages need to be installed. These packages are Bokeh, Numpy and Matplotlib. These

# blauw.smartgrid
Smart grid project van groep blauw (Thomas Reus, Daan Molleman en Harmke Vliek)

**Project**

The smart grid project exists of 150 houses and 5 batteries, anchored in a grid. The first phase of the project dictates a fixed location for both the houses and the batteries. All houses are in possession of some sort of green energy generator such as solar panels or windmills. The generators generate energy which has to be preserved in case the generated energy is not consumed immediately. This remaining energy is stored in one of the batteries using cable connections. The cables connecting the houses to the batteries and vice versa are constituted based on Manhattan distance, which means they cannot be set diagonally in the grid. The capacity of all batteries is limited. The first purpose of this project is connecting all the houses to the available batteries without exceeding the capacity of each battery. The second object is optimization of cable positioning which leads to the minimum amount of cable length needed to connect all houses and batteries. The third goal of this project is the minimalization of the cable length combined with the possibility of the installation of extra batteries and discover what is more beneficial; installing more batteries or developing an extensive cable network.

**Description**

The git is separated into two folders. The first one is code, in which our code resides. The second one is presentation. This map contains images, powerpoints and the UML diagram that represents the datastructure of the code.

**Complexity**
The Smart Grid problem is a complex one. To be able to calculate the state space of this problem, one needs a complexity function. The function for this specific problem is as follows: C = 𝐵^𝐻. C is complexity, b is the amount of houses and h is the amount of houses represented in the plot. The complexity for the three given grids is similar; 5^150 = 7,01 E104. Once the third goal is reached, it is possible to add extra batteries. This means that the state space will increase, as the value of variable B will be increased.

The upper and lower bounds of this case are defined in the amount of cost of the network. The upper and lower bound per grid are calculated including the fixed costs of the battery in the first two goals. These are rendered below.
![Upper and lower bound of the three grids](/Presentation/Images/bounds.png)

**Code**

__Constructive algorithms__
*Random*

![Random plot](/Presentation/Images/tryout_yfirst_alg0.png)
*Proximity first*

![Proximity first plot](/Presentation/Images/tryout_yfirst_alg0.png)
*Priority first*

![Priority first plot](/Presentation/Images/tryout_yfirst_alg0.png)

__Iterative algorithms__
*Hillclimber*

![Hillclimber plot](/Presentation/Images/tryout_yfirst_alg0.png)
*Simulated annealing*

![Simulated annealing plot](/Presentation/Images/tryout_yfirst_alg0.png)
*K-means*
![K-means algorithm plot](/Presentation/Images/tryout_yfirst.png)

The images shown above were created using matplotlib.pylot and Bokeh.

**Packages installed**
To run our code, several packages need to be installed. These packages are Bokeh, Numpy and Matplotlib. These

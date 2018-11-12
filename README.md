# blauw.smartgrid
Smart grid project van groep blauw (Thomas Reus, Daan Molleman en Harmke Vliek)

**Project**
The smart grid project exists of 150 houses and 5 batteries, anchored in a grid. The first phase of the project dictates a fixed location for both the houses and the batteries. All houses are in possession of some sort of green energy generator such as solar panels or windmills. The generators generate energy which has to be preserved in case the generated energy is not consumed immediately. This remaining energy is stored in one of the batteries using cable connections. The cables connecting the houses to the batteries and vice versa are constituted based on Manhattan distance, which means they cannot be set diagonally in the grid. The capacity of all batteries is limited. The first purpose of this project is connecting all the houses to the available batteries whitout exceeding the capacity of each battery. The second object is optimization of cable positioning which leads to the minimum amount of cable length needed to connect all houses and batteries. The third goal of this project is the minimalization of the cable length combined with the possibility of the installation of extra batteries and discover what is more beneficial; installing more batteries or developing an extensive cable network.

**Description**
The git is separated into two folders. The first one is code, in which our code resides. The second one is presentation. This map contains images, powerpoints and the UML diagram that represents the datastructure of the code.

**Code**
The current code exists of the creation of a grid in which the houses and batteries are stored. The locations of these houses and batteries are obtained from csv files. Connecting houses to batteries and vice versa is done based on the x, y coordinates stored in the properties of these objects. Furthermore, the cost of the total length of connections are calculated using the method of Manhattan distance.   

The first algorithm that we've programmed connects all houses to batteries without exceeding the capacity of the batteries. This because as soon as the maximum capacity of a battery is achieved, houses are connected to the next battery in line.
![Algoritme 1](/Presentation/Images/tryout_yfirst_alg0.png)

The second algorithm sorts houses based on distance with respect to the nearest battery. Houses with the smallest distance to a battery are first in the list, houses with larger distances to batteries are positioned later on. Batteries are connected to houses subsequently. When capacity of a battery is exceed or close to maximum, houses are tied to the next battery. 
![Algoritme 2](/Presentation/Images/tryout_yfirst.png)

The images shown above were created using matplotlib.pylot.

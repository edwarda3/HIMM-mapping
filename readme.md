**Mapping with exploration policy**

*Author: Alex Edwards*

*Date: Nov 19 2018*


Description:

This program implements a simulated robot using pygame which has imperfect sensors. It reads in a world file, which is an occupancy grid, and starting at (10,10), will start to explore the world. The world is mapped using Histogramic in-motion mapping (HIMM) and then converted to a map. 

We find a node to travel using a nearest neighbor filter on nodes that have a nonzero number of unknowns. The robot then takes that target node and runs A* search to find a way to get there. Using the function in Robot.moveToPoint(), we can store a list of points in the robot's navstack object and it will move to those points in order. Once it gets to the target, it recalculates a graph representation of a map based on the HIMM map, and repeats.
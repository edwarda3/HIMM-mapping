import math
import heapq
import time
import random

class Robot:
	xpos = 0
	ypos = 0
	theta = 0
	perfectRobot = False
	maxspeed = 3

	myMap = []
	map = {}
	candidates = {}
	navstack = []
	done = True

	def __init__(self,x,y,theta,world_width,world_height,probot):
		self.xpos = x
		self.ypos = y
		self.theta = theta
		#We are going to have a representation of the world into discrete bins 10 pixels wide.
		for _ in range(world_height//10):
			self.myMap.append([-1]*(world_width//10))
		self.perfectRobot = probot

	def spin(self):
		self.getNewRoute()

	# Old move. Unused, but allows movement with a vector <vel, thetavel>
	def move(self, vector, world):
		magnitude = vector[0]
		rads = vector[1]
		xmove = magnitude*math.cos(self.theta)
		ymove = magnitude*math.sin(self.theta)
		
		self.theta += rads
		if(self.theta < 0):
			self.theta += 2*math.pi 
		if(self.theta < (2*math.pi)):
			self.theta -= 2*math.pi

		if(not world.isInObstacle(self.xpos+xmove,self.ypos+ymove,False) and not world.outOfBounds(self.xpos+xmove,self.ypos+ymove)):
			self.xpos += xmove
			self.ypos += ymove

	#Generates a 4-connected map from the occupancy grid. Stored in a dict, where {(key=node): [list of connected nodes]}
	def getMap(self):
		for row in range(len(self.myMap)):
			for col in range(len(self.myMap[row])):
				if(self.myMap[row][col]<5 and self.myMap[row][col] >=0):
					if(not (row,col) in self.map):
						self.map[(row,col)] = []
					if(row-1>=0 and self.myMap[row-1][col] <5 and self.myMap[row-1][col] >=0):
						if(not (row-1,col) in self.map[(row,col)]):
							self.map[(row,col)].append((row-1,col))
					if(row+1<len(self.myMap) and self.myMap[row+1][col] <5 and self.myMap[row+1][col] >=0):
						if(not (row+1,col) in self.map[(row,col)]):
							self.map[(row,col)].append((row+1,col))
					if(col-1>=0 and self.myMap[row][col-1] <5 and self.myMap[row][col-1] >=0):
						if(not (row,col-1) in self.map[(row,col)]):
							self.map[(row,col)].append((row,col-1))
					if(col+1<len(self.myMap[row]) and self.myMap[row][col+1] <5 and self.myMap[row][col+1] >=0):
						if(not (row,col+1) in self.map[(row,col)]):
							self.map[(row,col)].append((row,col+1))
					if(row-1>=0 and col-1>=0 and self.myMap[row-1][col-1] <5 and self.myMap[row-1][col-1] >=0):
						if(not (row-1,col-1) in self.map[(row,col)] and (row-1,col) in self.map[(row,col)] and (row,col-1) in self.map[(row,col)]):
							self.map[(row,col)].append((row-1,col-1))
					if(row-1>=0 and col+1<len(self.myMap[row]) and self.myMap[row-1][col+1] <5 and self.myMap[row-1][col+1] >=0):
						if(not (row-1,col+1) in self.map[(row,col)] and (row-1,col) in self.map[(row,col)] and (row,col+1) in self.map[(row,col)]):
							self.map[(row,col)].append((row-1,col+1))
					if(row+1<len(self.myMap) and col+1<len(self.myMap[row]) and self.myMap[row+1][col+1] <5 and self.myMap[row+1][col+1] >=0):
						if(not (row+1,col+1) in self.map[(row,col)] and (row+1,col) in self.map[(row,col)] and (row,col+1) in self.map[(row,col)]):
							self.map[(row,col)].append((row+1,col+1))
					if(row+1<len(self.myMap) and col-1>=0 and self.myMap[row+1][col-1] <5 and self.myMap[row+1][col-1] >=0):
						if(not (row+1,col-1) in self.map[(row,col)] and (row+1,col) in self.map[(row,col)] and (row,col-1) in self.map[(row,col)]):
							self.map[(row,col)].append((row+1,col-1))

	#Calculcates the rank of a tile as defined in getNodeWithMostUnexplored.
	#negative = more unexplored
	def aggVal(self,node):
		(row,col) = node
		val = 0
		if(row-1>=0):
			val += min(0,self.myMap[row-1][col])
		if(row+1<len(self.myMap)):
			val += min(0,self.myMap[row+1][col])
		if(col-1>=0):
			val += min(0,self.myMap[row][col-1])
		if(col+1<len(self.myMap[row])):
			val += min(0,self.myMap[row][col+1])
		return val

	# Finds a suitable node for the target of A*.
	# The algorithm works in 3 steps:
	#	 First, rank all the nodes with the number of adjacent unknown nodes next to them. Because unknowns are -1, the more negative the number, the higher rank.
	# Using the highest ranked list with any nodes (up to -2, because -3 or -4 has a high probability of not having any connecting paths), find the closest node in that list using manhattan distance.
	# If 0 is the highest rank, then just choose a random node.
	# This function also features exclusion nodes. If the A* search could not find any path to the target, then it will call this function again and have that node excluded from the results.
	def getNodeWithMostUnexplored(self,start,exclusion):
		self.candidates = {}
		#Iterate through the robot's map
		for row in range(len(self.myMap)):
			for col in range(len(self.myMap[row])):
				# Only allow candidates if the tile is open and known.
				if(self.myMap[row][col]<5 and self.myMap[row][col] >=0):
					importance = self.aggVal((row,col))
					if(not importance in self.candidates):
						self.candidates[importance] = []
					self.candidates[importance].append((row,col))

		# Exclude nodes that were told to be unreachable.
		for badnode in exclusion:
			for i in range(-2,0):
				if(i in self.candidates):
					if(badnode in self.candidates[i]):
						self.candidates[i].remove(badnode)

		#Get the nearest node with the highest rank.
		listCand = []
		if(-2 in self.candidates):
			listCand.extend(self.candidates[-2])
		if(-1 in self.candidates):
			listCand.extend(self.candidates[-1])
		if(len(listCand) > 0):
			#print("Candidates["+str(i)+"] is choosing from "+str(len(self.candidates[i])))
			#print("Candidates: \n"+str(self.candidates[i])+"\nexcluding:\n"+str(exclusion))
			shortestpoint = listCand[0]
			smallestdist = self.aStarHeuristic(start,shortestpoint)
			for point in listCand:
				dist = self.aStarHeuristic(start,point)
				if(dist < smallestdist):
					smallestdist = dist
					shortestpoint = point
			choice = shortestpoint
			#print("New target: "+str(choice))
			return choice, exclusion
		#If 0 is the highest rank, just random.
		if(not -1 in self.candidates and not -2 in self.candidates):
			choice = random.choice(self.candidates[0])
			#print("New target: "+str(choice))
			return choice, exclusion

	def getCurPos(self):
		return (min(len(self.myMap),max(0,int(self.ypos//10))),min(len(self.myMap[0]),max(0,int(self.xpos//10))))

	#Manhattan distance between @param origin, @param target
	def aStarHeuristic(self,origin,target):
		(y1,x1) = origin
		(y2,x2) = target
		return math.sqrt((x2-x1)**2+(y2-y1)**2)

	# Implementation of A* search, copied from HW4, with one modification.
	# This function allows a lost of nodes to exclude from searching, as they may not have a path to them. This allows A* to call itself with a new target in case it couldn't find the one given.
	def astar(self,start,target, ex):
		print("Finding a way from "+str((start)) + " to " + str((target)))
		unvisited = []	# Contains the frontier, these nodes will have a estimated cost associated with them, which is the real cost that we found, + estimated cost from the heuristic. We will use a heapq, which is a priority queue implementation.
		backtrack = {}
		
		cost = {}		# The cost dictionary will contain the cost to go to the indexed node from the start.

		heapq.heappush(unvisited,(0,start))
		backtrack[start] = start
		cost[start] = 0

		current = (0,0)
		while(not current==target and len(unvisited)>0):
			(_, current) = heapq.heappop(unvisited) 	# This is retrieved like this because our heapq contains a tuple of cost and point.

			# Expand the lowest cost leaf node to reveal more leaf nodes.
			for next in self.map[current]:
				foundcost = self.aStarHeuristic(current,next)+cost[current] 	

				if(next not in cost or foundcost<cost[next]):	# We only want to add the frontier node again if its cheaper. Otherwise, add it if we havent seen this node yet.
					cost[next] = foundcost		# If it is cheaper, use this as the cost. If its the first time, use it as the cost.
					estcost = cost[next] + self.aStarHeuristic(next,target)
					heapq.heappush(unvisited,(estcost,next))
					backtrack[next] = current	# Update the backtrack queue to store our paths.
					""" if(next==target):
						print("\tPotential to get to target: " +str(current) + "->"+str(next)) """

		if(not target in backtrack):
			print("Could not find a way to "+ str(target)+", adding to exclusion and finding new goal")
			ex.append(target)
			newtarget, ex = self.getNodeWithMostUnexplored(start,ex)
			return self.astar(start,newtarget,ex)
		#print(str(backtrack))
		return backtrack, cost, target

	# Returns a path, in order, from the current position @param start, to the target position @param target.
	# Uses a backtrack list from a graph search algorithm, in this case, A*
	def sendPath(self,backtrack,cost,start,target):
		#print("Getting path from "+str(target) +" to "+str(start))
		traverse = target
		list = []
		list.insert(0,traverse)
		while(not traverse == start):
			#print("-> From "+str(traverse) +" to "+str(backtrack[traverse]))
			list.insert(0,backtrack[traverse])
			traverse = backtrack[traverse]
		return list

	#Print functions...
	def printMap(self,map):
		s = ""
		for point in map:
			if(len(map[point]) > 0):
				s += str(point) + ": " + str(map[point]) + "\n"
		return s
	def printDict(self,dict):
		s = ""
		for point in dict:
			s += str(point) + ": " + str(dict[point]) + "\n"
		return s

	# A wrapper function to call other functions.
	# Will Update the map, get a new target node, get a path between the current pos and target, and refine that backtrack list from A* into an actual list for navstack to use.
	def getNewRoute(self):
		print("---\nGetting a new route...\n\n")
		self.getMap()
		curPos = self.getCurPos()
		#print("My Current Position: "+str(curPos))
		#print("My Current Map: \n"+self.printMap(self.map))
		target, _ = self.getNodeWithMostUnexplored(curPos,[])
		backtrack, cost, target = self.astar(curPos,target,[])
		#print("My BT List: "+ self.printDict(backtrack))
		self.navstack = self.sendPath(backtrack,cost,curPos,target)
		self.moveToPoint()

	# An abstracted move function
	# Moves some distance between two points, must be called iteratively, as to not block the pygame drawing.
	# The points are stored in navstack, and once its empty, will call for a new set of points.
	def moveToPoint(self):
		(y,x) = (self.ypos,self.xpos)
		if(len(self.navstack) > 0):
			point = self.navstack[0]
			#print("Moving to "+str(point))
			(y,x) = point
			x = x*10 #convert from node to position
			y = y*10
		if(abs(self.xpos-x) > 5 or abs(self.ypos-y) > 5):
			mVector = (x-self.xpos, y-self.ypos)
			self.theta = math.atan2(mVector[1],mVector[0])
			magnitude = math.sqrt((mVector[0])**2 + mVector[1]**2)
			xmove = magnitude*math.cos(self.theta)
			ymove = magnitude*math.sin(self.theta)
			#print(str((xmove,ymove)))
			self.xpos += xmove
			self.ypos += ymove
		else:
			if(len(self.navstack) > 0):
				self.navstack.pop(0)
			if(len(self.navstack) == 0):
				self.getNewRoute()

	# Gets sensor readings from 360 degrees around me, starting from behind, and adding .05 radians every time. The stepping value is arbitrary.
	def get_sensor_readings(self,world):
		angleStep = .05
		curAngle = - (math.pi)
		while(curAngle < (math.pi)):
			x = self.xpos
			y = self.ypos
			a = self.theta + curAngle
			# We are going to project a line out from the robot, and each step, we check with our sensor (world.isInObstacle) to see if we are in an obstacle. As soon as it returns true, we "cant see" past it, and immediately go to the next angle increment
			# We use HIMM here, breaking the map into discrete bins and having values from 0-15 here. Although this is originally meant for saving space by having each value be half a bit, they will be floating point values here because we can afford it. Getting a signal that something is there will increment that bin by 1 and stop. If we pass through, then we decrement that bin by 0.5. The probability can be thought of as bin/15.
			while(x < world.x_bound and x > 0 and y<world.y_bound and y>0):
				if(self.myMap[int(y//10)][int(x//10)] ==-1):
					self.myMap[int(y//10)][int(x//10)] = 7
				if(world.isInObstacle(x,y,self.perfectRobot)):
					self.myMap[int(y//10)][int(x//10)] = min(self.myMap[int(y//10)][int(x//10)]+2, 15)
					break
				else:
					self.myMap[int(y//10)][int(x//10)] = max(self.myMap[int(y//10)][int(x//10)]-2, 0)
				x += 5*math.cos(a)
				y += 5*math.sin(a)

			curAngle += angleStep
		self.gotNewInfo = True

	# returns an array of points that can be passed into pygame.draw.polygon()
	def get_drawable_poly(self):
		toppoint = (self.xpos + 8*math.cos(self.theta), self.ypos + 8*math.sin(self.theta))
		sidepoint1 = (self.xpos + 5*math.cos(self.theta + (3*math.pi/4)), self.ypos + 5*math.sin(self.theta + (3*math.pi/4)))
		sidepoint2 = (self.xpos + 5*math.cos(self.theta + (5*math.pi/4)), self.ypos + 5*math.sin(self.theta + (5*math.pi/4)))
		midpoint = (self.xpos - 2*math.cos(self.theta), self.ypos - 2*math.sin(self.theta))
		return [toppoint,sidepoint1,midpoint,sidepoint2]

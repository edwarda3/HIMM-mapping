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

	def aggVal(self,node):
		(row,col) = node
		val = 0
		if(row-1>=0):
			val += self.myMap[row-1][col]
		if(row+1<len(self.myMap)):
			val += self.myMap[row+1][col]
		if(col-1>=0):
			val += self.myMap[row][col-1]
		if(col+1<len(self.myMap[row])):
			val += self.myMap[row][col+1]
		return val

	def getNodeWithMostUnexplored(self,start,exclusion):
		self.candidates = {}
		for row in range(len(self.myMap)):
			for col in range(len(self.myMap[row])):
				if(self.myMap[row][col]<5 and self.myMap[row][col] >=0):
					importance = self.aggVal((row,col))
					if(not importance in self.candidates):
						self.candidates[importance] = []
					self.candidates[importance].append((row,col))

		for badnode in exclusion:
			for i in range(-2,0):
				if(i in self.candidates):
					if(badnode in self.candidates[i]):
						self.candidates[i].remove(badnode)
		for i in range(-2,0):
			if(i in self.candidates):
				if(len(self.candidates[i]) > 0):
					#print("Candidates["+str(i)+"] is choosing from "+str(len(self.candidates[i])))
					#print("Candidates: \n"+str(self.candidates[i])+"\nexcluding:\n"+str(exclusion))
					shortestpoint = self.candidates[i][0]
					smallestdist = self.aStarHeuristic(start,shortestpoint)
					for point in self.candidates[i]:
						dist = self.aStarHeuristic(start,point)
						if(dist < smallestdist):
							smallestdist = dist
							shortestpoint = point
					choice = shortestpoint
					#print("New target: "+str(choice))
					return choice, exclusion
		if(not -1 in self.candidates and not -2 in self.candidates):
			choice = random.choice(self.candidates[0])
			#print("New target: "+str(choice))
			return choice, exclusion

	def getCurPos(self):
		return (int(self.ypos//10),int(self.xpos//10))

	def aStarHeuristic(self,origin,target):
		(y1,x1) = origin
		(y2,x2) = target
		return math.sqrt((x2-x1)**2+(y2-y1)**2)

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
				foundcost = 1+cost[current] 	# since edge costs are 1, cost from current to next is 1

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

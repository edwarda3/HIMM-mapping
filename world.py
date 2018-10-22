import random
class World:
	x_bound = 0
	y_bound = 0
	obstacles = []

	def __init__(self,x_bound,y_bound):
		self.x_bound = x_bound
		self.y_bound = y_bound

	def addObstacle(self, point1, point2):
		if(point1[0] < point2[0] and point1[1] < point2[1]):
			self.obstacles.append((point1,point2))
			return True
		else:
			return False
	
	def isInObstacle(self, x, y):
		for ob in self.obstacles:
			if(x >= ob[0][0] and x <= ob[1][0] and y >= ob[0][1] and y <= ob[1][1]): #if actually in an obstacle
				if(random.random()<.85): # add some uncertainly to make it more realistic
					return True
				else:
					return False
		if(random.random() < .95): # if the sensor doesnt see anything, p=.9 to report properly
			return False
		else:
			return True
import random
import mObstacle
class World:
	x_bound = 0
	y_bound = 0
	obstacles = []
	movingObstacles = []

	def __init__(self,x_bound,y_bound):
		self.x_bound = x_bound
		self.y_bound = y_bound

	def addObstacle(self, point1, point2):
		if(point1[0] < point2[0] and point1[1] < point2[1]):
			self.obstacles.append((point1,point2))
			return True
		else:
			return False

	def addMovingObstacle(self, point1, point2, endpoint1, endpoint2, speed):
		if(point1[0] < point2[0] and point1[1] < point2[1]):
			mo = mObstacle.mObstacle(point1,point2,endpoint1,endpoint2,speed)
			self.movingObstacles.append(mo)
			return True
		else:
			return False
	
	# @param perfect: pass True to have perfectly accurate data.
	def isInObstacle(self, x, y, perfect):
		for ob in self.obstacles:
			if(x >= ob[0][0] and x <= ob[1][0] and y >= ob[0][1] and y <= ob[1][1]): #if actually in an obstacle
				if(not perfect):
					if(random.random()<.9): # add some uncertainly to make it more realistic
						return True
					else:
						return False
				else:
					return True
		for mob in self.movingObstacles:
			if(mob.isInMe(x,y)): #if in an moving obstacle
				if(not perfect):
					if(random.random()<.9): # add some uncertainly to make it more realistic
						return True
					else:
						return False
				else:
					return True
		if(not perfect):
			if(random.random() < .95): # if the sensor doesnt see anything, p=.9 to report properly
				return False
			else:
				return True
		else:
			return False

	def outOfBounds(self,x,y):
		if(x>self.x_bound or x<0):
			return True
		if(y>self.y_bound or y<0):
			return True
		return False
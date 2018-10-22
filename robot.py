import math

class Robot:
	xpos = 0
	ypos = 0
	theta = 0
	step = 5

	myMap = []

	def __init__(self,x,y,theta,world_width,world_height):
		self.xpos = x
		self.ypos = y
		self.theta = theta
		for _ in range(world_height//10):
			self.myMap.append([15]*(world_width//10))

	def isSpaceInFrontClear(self,world):
		xFront = self.xpos + (10*math.cos(self.theta))
		yFront = self.xpos + (10*math.sin(self.theta))
		return world.isInObstacle(xFront,yFront)

	def moveforward(self):
		xmove = self.step*math.cos(self.theta)
		ymove = self.step*math.sin(self.theta)

		self.xpos += xmove
		self.ypos += ymove

	def turn(self, rads):
		self.theta += rads
		if(self.theta < 0):
			self.theta += 2*math.pi 
		if(self.theta < (2*math.pi)):
			self.theta -= 2*math.pi

	def get_sensor_readings(self,world):
		angleStep = .05
		curAngle = - (math.pi)
		while(curAngle < (math.pi)):
			x = self.xpos
			y = self.ypos
			a = self.theta + curAngle
			while(x < world.x_bound and x > 0 and y<world.y_bound and y>0):
				if(world.isInObstacle(x,y)):
					self.myMap[int(y//10)][int(x//10)] = min(self.myMap[int(y//10)][int(x//10)]+.3, 15)
					break
				else:
					self.myMap[int(y//10)][int(x//10)] = max(self.myMap[int(y//10)][int(x//10)]-.3, 0)
				x += 2*math.cos(a)
				y += 2*math.sin(a)

			curAngle += angleStep
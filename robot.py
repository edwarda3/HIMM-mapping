import math

class Robot:
	xpos = 0
	ypos = 0
	theta = 0
	perfectRobot = False

	myMap = []

	def __init__(self,x,y,theta,world_width,world_height,probot):
		self.xpos = x
		self.ypos = y
		self.theta = theta
		#We are going to have a representation of the world into discrete bins 10 pixels wide.
		for _ in range(world_height//10):
			self.myMap.append([15]*(world_width//10))
		self.perfectRobot = probot

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
				if(world.isInObstacle(x,y,self.perfectRobot)):
					self.myMap[int(y//10)][int(x//10)] = min(self.myMap[int(y//10)][int(x//10)]+1, 15)
					break
				else:
					self.myMap[int(y//10)][int(x//10)] = max(self.myMap[int(y//10)][int(x//10)]-.5, 0)
				x += 5*math.cos(a)
				y += 5*math.sin(a)

			curAngle += angleStep

	# returns an array of points that can be passed into pygame.draw.polygon()
	def get_drawable_poly(self):
		toppoint = (self.xpos + 8*math.cos(self.theta), self.ypos + 8*math.sin(self.theta))
		sidepoint1 = (self.xpos + 5*math.cos(self.theta + (3*math.pi/4)), self.ypos + 5*math.sin(self.theta + (3*math.pi/4)))
		sidepoint2 = (self.xpos + 5*math.cos(self.theta + (5*math.pi/4)), self.ypos + 5*math.sin(self.theta + (5*math.pi/4)))
		midpoint = (self.xpos - 2*math.cos(self.theta), self.ypos - 2*math.sin(self.theta))
		return [toppoint,sidepoint1,midpoint,sidepoint2]

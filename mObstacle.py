class mObstacle:
	startingpoint1 = (0,0)
	startingpoint2 = (0,0)
	endingpoint1 = (0,0)
	endingpoint2 = (0,0)
	speed = 0
	counter = 0
	currentpoint1 = [0,0]
	currentpoint2 = [0,0]
	moveToEnd = True
	stepdiv = 1000

	def __init__(self,sp1,sp2,ep1,ep2,v):
		self.startingpoint1 = sp1
		self.startingpoint2 = sp2
		self.endingpoint1 = ep1
		self.endingpoint2 = ep2
		self.speed = v
		self.currentpoint1[0] = sp1[0]
		self.currentpoint1[1] = sp1[1]
		self.currentpoint2[0] = sp2[0]
		self.currentpoint2[1] = sp2[1]

	def move(self):
		dx1=dy1=dx2=dy2=0
		if(self.moveToEnd):
			dx1 = (self.endingpoint1[0] - self.startingpoint1[0])*(self.speed*(1/self.stepdiv))
			dy1 = (self.endingpoint1[1] - self.startingpoint1[1])*(self.speed*(1/self.stepdiv))
			dx2 = (self.endingpoint2[0] - self.startingpoint2[0])*(self.speed*(1/self.stepdiv))
			dy2 = (self.endingpoint2[1] - self.startingpoint2[1])*(self.speed*(1/self.stepdiv))
			
			self.counter += self.speed
		elif(not self.moveToEnd):
			dx1 = (self.startingpoint1[0] - self.endingpoint1[0])*(self.speed*(1/self.stepdiv))
			dy1 = (self.startingpoint1[1] - self.endingpoint1[1])*(self.speed*(1/self.stepdiv))
			dx2 = (self.startingpoint2[0] - self.endingpoint2[0])*(self.speed*(1/self.stepdiv))
			dy2 = (self.startingpoint2[1] - self.endingpoint2[1])*(self.speed*(1/self.stepdiv))
			self.counter -= self.speed

		if(self.counter < 0 and not self.moveToEnd):
			self.moveToEnd = True
		if(self.counter > self.stepdiv and self.moveToEnd):
			self.moveToEnd = False

		self.currentpoint1[0] += dx1
		self.currentpoint1[1] += dy1
		self.currentpoint2[0] += dx2
		self.currentpoint2[1] += dy2
		
	def isInMe(self,x,y):
		if(x > self.currentpoint1[0] and x < self.currentpoint2[0] and y > self.currentpoint1[1] and y < self.currentpoint2[1]):
			return True
		else:
			return False

	def get_drawable_rect(self):
		return (self.currentpoint1, (self.currentpoint2[0]-self.currentpoint1[0], self.currentpoint2[1]-self.currentpoint1[1]))
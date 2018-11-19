import pygame
import sys
import time
import random
import math

import world
import robot

wWidth = 800
wHeight = 600

# If perfectRobot is true, then the sensor data has no error.
perfectRobot = False

# hardcoded function to add some obstacles
def addObs(world):
	world.addObstacle((50,50),(100,550))
	world.addObstacle((100,100),(250,150))
	world.addObstacle((200,0),(500,50))
	world.addObstacle((300,50),(350,250))
	world.addObstacle((170,220),(270,320))
	world.addObstacle((200,550),(800,600))
	world.addObstacle((500,100),(550,550))
	world.addObstacle((550,100),(750,150))
	world.addObstacle((700,150),(750,500))
	world.addObstacle((600,300),(700,350))
	world.addObstacle((600,0),(800,50))

if __name__ == "__main__":
	w = world.World(wWidth,wHeight)
	addObs(w)
	rob = robot.Robot(380,220,0,w.x_bound,w.y_bound,perfectRobot)
	v = [0,0] # <v,theta>
	
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Ariel', 12)
	screen = pygame.display.set_mode((w.x_bound,w.y_bound))

	rob.get_sensor_readings(w)
	while(True):
		screen.fill((220,220,220))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

			""" #Arrow key movement simply changes the velocity vector.
			if(event.type == pygame.KEYDOWN): 
				if(event.key == pygame.K_UP):
					v[0] = 3
				if(event.key == pygame.K_LEFT):
					v[1] = -.05
				if(event.key == pygame.K_RIGHT):
					v[1] = .05
			if(event.type == pygame.KEYUP): 
				if(event.key == pygame.K_UP):
					v[0] = 0
				if(event.key == pygame.K_LEFT):
					v[1] = 0
				if(event.key == pygame.K_RIGHT):
					v[1] = 0 """

		rob.moveToPoint()

		#rob.move(v,w)
		rob.get_sensor_readings(w)

		# Drawing the robot's map. This is defined in robot.py.
		for y in range(len(rob.myMap)):
			for x in range(len(rob.myMap[y])):
				mapvis = pygame.Rect((x*10,y*10),(10,10))
				wallprob = int(rob.myMap[y][x] * 10)
				if(wallprob < 50 and wallprob > 0): wallprob = 0 #Color smoothing
				color = (160-wallprob,160-wallprob,160-wallprob)
				if(wallprob == -10):
					color = (160,100,100)
				pygame.draw.rect(screen,color,mapvis,0)

		for key in rob.map:
			for edge in rob.map[key]:
				color = (20,50,160)
				start = (key[1]*10,key[0]*10)
				end = (edge[1]*10,edge[0]*10)
				pygame.draw.line(screen,color,start,end,1)

		for i in range(len(rob.navstack)):
			if(i+1<len(rob.navstack)):
				color = (20,160,50)
				start = (rob.navstack[i][1]*10,rob.navstack[i][0]*10)
				end = (rob.navstack[i+1][1]*10,rob.navstack[i+1][0]*10)
				pygame.draw.line(screen,color,start,end,2)
			else:
				color = (160,20,50)
				point = (rob.navstack[i][1]*10,rob.navstack[i][0]*10)
				pygame.draw.circle(screen,color,point,5)

		for rank in range(-2,1):
			if(rank in rob.candidates):
				for point in rob.candidates[rank]:
					color = (153, 102, 51)
					if(rank==-2):
						color = (255, 102, 0)
					if(rank==-1):
						color = (255, 153, 0)
					point = (point[1]*10,point[0]*10)
					pygame.draw.circle(screen,color,point,3)


		""" for ob in w.obstacles:
			r = pygame.Rect(ob[0],(ob[1][0]-ob[0][0], ob[1][1]-ob[0][1]))
			pygame.draw.rect(screen,(0,250,0),r,0) """
		""" for ob in w.movingObstacles:
			ob.move()
			r = ob.get_drawable_rect()
			pygame.draw.rect(screen,(0,250,0),r,0)  """
			
		robPoly = rob.get_drawable_poly()
		pygame.draw.polygon(screen,(200,40,40),robPoly,0)



		pygame.display.update()

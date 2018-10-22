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

	world.addMovingObstacle((100,250),(500,300),(100,500),(350,550),1)

if __name__ == "__main__":
	w = world.World(wWidth,wHeight)
	addObs(w)
	rob = robot.Robot(370,220,0,w.x_bound,w.y_bound,perfectRobot)
	v = [0,0] # <v,theta>
	
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Ariel', 12)
	screen = pygame.display.set_mode((w.x_bound,w.y_bound))


	while(True):
		screen.fill((220,220,220))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

			#Arrow key movement simply changes the velocity vector.
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
					v[1] = 0


		rob.move(v,w)
		rob.get_sensor_readings(w)

		# Drawing the robot's map. This is defined in robot.py.
		for y in range(len(rob.myMap)):
			for x in range(len(rob.myMap[y])):
				mapvis = pygame.Rect((x*10,y*10),(10,10))
				wallprob = int(rob.myMap[y][x] * 10)
				if(wallprob < 30): wallprob = 0 #Color smoothing
				color = (160-wallprob,160-wallprob,160-wallprob)
				pygame.draw.rect(screen,color,mapvis,0)

		""" for ob in w.obstacles:
			r = pygame.Rect(ob[0],(ob[1][0]-ob[0][0], ob[1][1]-ob[0][1]))
			pygame.draw.rect(screen,(0,250,0),r,0) """
		""" for ob in w.movingObstacles:
			ob.move()
			r = ob.get_drawable_rect()
			pygame.draw.rect(screen,(0,250,0),r,0)  """

		for mob in w.movingObstacles:
			mob.move()
			
		robPoly = rob.get_drawable_poly()
		pygame.draw.polygon(screen,(200,40,40),robPoly,0)



		pygame.display.update()

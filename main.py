import pygame
import sys
import time
import random
import math

import world
import robot

wWidth = 800
wHeight = 600

def addObs(world):
	world.addObstacle((100,100),(200,200))
	world.addObstacle((150,400),(200,600))
	world.addObstacle((250,200),(300,250))
	world.addObstacle((400,100),(550,250))
	world.addObstacle((200,500),(300,550))

if __name__ == "__main__":
	w = world.World(wWidth,wHeight)
	addObs(w)
	rob = robot.Robot(300,300,0,w.x_bound,w.y_bound)

	
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

			if(event.type == pygame.KEYDOWN): 
				if(event.key == pygame.K_UP):
					rob.moveforward()	
				if(event.key == pygame.K_LEFT):
					rob.turn(-.1)
				if(event.key == pygame.K_RIGHT):
					rob.turn(.1)

		for ob in w.obstacles:
			r = pygame.Rect(ob[0],(ob[1][0]-ob[0][0], ob[1][1]-ob[0][1]))
			pygame.draw.rect(screen,(0,250,0),r,0)

		rob.get_sensor_readings(w)


		for y in range(len(rob.myMap)):
			for x in range(len(rob.myMap[y])):
				mapvis = pygame.Rect((x*10,y*10),(10,10))
				wallprob = int(rob.myMap[y][x] * 10)
				color = (160-wallprob,160-wallprob,160-wallprob)
				pygame.draw.rect(screen,color,mapvis,0)

		robRect = pygame.Rect((rob.xpos-2,rob.ypos-2),(4,4))
		pygame.draw.rect(screen,(200,40,40),robRect,0)


		pygame.display.update()

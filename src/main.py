# Title: Mapping with exploration policy
# Author: Alex Edwards
# Date: Nov 19 2018
# Description:
#	This program implements a simulated robot using pygame which has imperfect sensors. It reads in a world file, which is an occupancy grid, and starting at (10,10), will start to explore the world. The world is mapped using Histogramic in-motion mapping (HIMM) and then converted to a map. We find a node to travel using a nearest neighbor filter on nodes that have a nonzero number of unknowns. The robot then takes that target node and runs A* search to find a way to get there. Using the function in Robot.moveToPoint(), we can store a list of points in the robot's navstack object and it will move to those points in order. Once it gets to the target, it recalculates a graph representation of a map based on the HIMM map, and repeats.

import pygame
import sys
import time
import random
import math
import argparse
import os

import world
import robot

wWidth = 800
wHeight = 600
s_legend = 300

settings = {"map-edges": False,
			"path": True,
			"target": True,
			"target-candidates": True}

# If perfectRobot is true, then the sensor data has no error.
perfectRobot = False

# hardcoded function to add some obstacles

def getMapFromFile(filepath):
	rows,cols = 30,40
	data = ""
	occgrid = [[0 for _ in range(cols)] for _ in range(rows)]

	#boilerplace read file
	print("Reading file... ", end = '')
	try:
		myfile = open(filepath,'r')
	except IOError:
		print("Failed to read file!")
		sys.exit()
	with myfile:
		data = myfile.read()
	print("Done!")
	#change occupancy grid from string to matrix 
	for i in range(len(data)):
		if(data[i]=='1'):
			occgrid[(i//2)//cols][(i//2)%cols] = 1
		if(data[i]=='0'):
			occgrid[(i//2)//cols][(i//2)%cols] = 0
	return occgrid

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen,text,font,color,x,y,):
    TextSurf, TextRect = text_objects(text, font, color)
    TextRect.top = y
    TextRect.left = x
    screen.blit(TextSurf, TextRect)

def drawLegend(screen,font):
	leftOffset = wWidth+60
	topOffset = 100

	bigfont = pygame.font.SysFont('Ariel', 40)
	message_display(screen,"Legend", bigfont, (0,0,0), leftOffset+15,50)
	
	# Unknown tiles
	pygame.draw.rect(screen,(160,100,100),pygame.Rect(leftOffset,topOffset,10,10),0)
	message_display(screen,"Unknown Tiles", font, (0,0,0), leftOffset+30,topOffset)

	for i in range(15):
		pygame.draw.rect(screen,(160-(i*10),160-(i*10),160-(i*10)),pygame.Rect(leftOffset+(i*10),topOffset+50,10,10),0)
	message_display(screen,"Occupancy Grid", font, (0,0,0), leftOffset,topOffset+65)
	message_display(screen,"Darker = Wall", font, (0,0,0), leftOffset,topOffset+80)
	
	mapc = (0,0,0)
	if(not settings["map-edges"]): mapc = (140,140,140)
	message_display(screen,"(M)", font, mapc, leftOffset-30,topOffset+120)
	pygame.draw.line(screen,(20,50,160),(leftOffset,topOffset+125),(leftOffset+20,topOffset+125),1)
	message_display(screen,"Map Edge", font, (0,0,0), leftOffset+40,topOffset+120)

	pathc = (0,0,0)
	if(not settings["path"]): pathc = (140,140,140)
	message_display(screen,"(P)", font, pathc, leftOffset-30,topOffset+180)
	pygame.draw.line(screen,(20,160,50),(leftOffset,topOffset+185),(leftOffset+20,topOffset+185),1)
	message_display(screen,"Active Path", font, (0,0,0), leftOffset+40,topOffset+180)

	targetc = (0,0,0)
	if(not settings["path"]): targetc = (140,140,140)
	message_display(screen,"(T)", font, targetc, leftOffset-30,topOffset+240)
	pygame.draw.circle(screen,(160,20,50),(leftOffset+3,topOffset+245),6)
	message_display(screen,"Active Target", font, (0,0,0), leftOffset+20,topOffset+240)

	targetcandc = (0,0,0)
	if(not settings["path"]): targetcandc = (140,140,140)
	message_display(screen,"(C)", font, targetcandc, leftOffset-30,topOffset+320)

	pygame.draw.circle(screen,(255, 102, 0),(leftOffset+3,topOffset+305),6)
	message_display(screen,">2 Adjacent Unknowns", font, (0,0,0), leftOffset+20,topOffset+300)
	message_display(screen,"Candidate for target", font, (0,0,0), leftOffset+25,topOffset+315)

	pygame.draw.circle(screen,(255, 153, 0),(leftOffset+3,topOffset+365),6)
	message_display(screen,"1 Adjacent Unknown", font, (0,0,0), leftOffset+20,topOffset+340)
	message_display(screen,"Candidate for target", font, (0,0,0), leftOffset+25,topOffset+355)


	#message_display(screen,"© Alex Edwards, 2018", font, wWidth+s_legend-170,wHeight-20)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("worldfile", help="World csv file. You can generate one using the worlds/makeMap.py program!")
	args=parser.parse_args()
	wfile = args.worldfile
	cwd = os.getcwd()

	w = world.World(wWidth,wHeight)
	w.addObstaclesFromOccGrid(getMapFromFile(cwd+"/"+wfile))
	rob = robot.Robot(10,10,0,w.x_bound,w.y_bound,perfectRobot)
	
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Ariel', 20)
	screen = pygame.display.set_mode((w.x_bound+s_legend,w.y_bound))

	screen.fill((220,220,220))
	drawLegend(screen,myfont)

	rob.get_sensor_readings(w)
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

			if(event.type == pygame.KEYDOWN): 
				if(event.key == pygame.K_m):
					settings["map-edges"] = not settings["map-edges"]
				if(event.key == pygame.K_p):
					settings["path"] = not settings["path"]
				if(event.key == pygame.K_t):
					settings["target"] = not settings["target"]
				if(event.key == pygame.K_c):
					settings["target-candidates"] = not settings["target-candidates"]
				if(event.key == pygame.K_a):
					boolean = (settings["map-edges"] or settings["map-edges"] or settings["target"] or settings["target-candidates"])
					print(str(boolean))
					settings["map-edges"] = not boolean
					settings["path"] = not boolean
					settings["target"] = not boolean
					settings["target-candidates"] = not boolean
				drawLegend(screen,myfont)

		rob.moveToPoint()
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

		if(settings["map-edges"]):
			for key in rob.map:
				for edge in rob.map[key]:
					color = (20,50,160)
					start = (key[1]*10,key[0]*10)
					end = (edge[1]*10,edge[0]*10)
					pygame.draw.line(screen,color,start,end,1)

		for i in range(len(rob.navstack)):
			if(i+1<len(rob.navstack)):
				if(settings["path"]):
					color = (20,160,50)
					start = (rob.navstack[i][1]*10,rob.navstack[i][0]*10)
					end = (rob.navstack[i+1][1]*10,rob.navstack[i+1][0]*10)
					pygame.draw.line(screen,color,start,end,2)
			else:
				if(settings["target"]):
					color = (160,20,50)
					point = (rob.navstack[i][1]*10,rob.navstack[i][0]*10)
					pygame.draw.circle(screen,color,point,5)

		if(settings["target-candidates"]):
			for rank in range(-2,0):
				if(rank in rob.candidates):
					for point in rob.candidates[rank]:
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

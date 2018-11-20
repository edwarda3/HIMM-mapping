import sys
import pygame

ROWS = 30
COLS = 40
PIXELDIM = 20

S_WIDTH = COLS*PIXELDIM
S_HEIGHT = ROWS*PIXELDIM

def getGrid(screen):
	grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
	for row in range(ROWS):
		for col in range(COLS):
			if(screen.get_at((col*PIXELDIM,row*PIXELDIM)) == (0,0,0,255)):
				grid[row][col] = 1

	return grid

def strGrid(grid):
	string = ''
	comma = True
	for row in grid:
		comma = False
		for occ in row:
			if(comma):
				string+=','
			string+=str(occ)
			comma = True
		string+='\n'
	return string

if __name__ == "__main__":
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Ariel', 12)
	screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
	screen.fill((255,255,255))

	pressed=False
	while(True):
		m1,m2,m3 = pygame.mouse.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() 
				sys.exit()

			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_SPACE):
					grid = getGrid(screen)
					print(strGrid(grid))

		(x,y) = pygame.mouse.get_pos()
		row = x//PIXELDIM
		col = y//PIXELDIM
		if(m1):
			rect = pygame.Rect(((row*PIXELDIM),(col*PIXELDIM)),(PIXELDIM,PIXELDIM))
			pygame.draw.rect(screen,(0,0,0),rect)
		if(m3):
			rect = pygame.Rect(((row*PIXELDIM),(col*PIXELDIM)),(PIXELDIM,PIXELDIM))
			pygame.draw.rect(screen,(255,255,255),rect)
		pygame.display.update()
		
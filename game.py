import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800

CAR_IMG = pygame.image.load("C:/Car/car.png")
WALL_IMG = [pygame.image.load("C:/Car/wall.jpg")]
BG_IMG = pygame.image.load("C:/Car/bg.jpg")

STAT_FONT = pygame.font.SysFont("comicsans", 50)

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

class Car:
	IMG = CAR_IMG

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.img = self.IMG

	def draw(self, win):
		win.blit(self.img, (self.x, self.y))

class Wall:
	VEL = 5

	def __init__(self, y):
		self.y = y

		self.pos = random.randrange(0, 600, 200)
		self.WALL = WALL_IMG[0]

		self.passed = False

	def move(self):
		self.y += self.VEL

	def draw(self, win):
		win.blit(self.WALL, (self.pos, self.y))

	def collide(self, car, wall):
		if car.y == wall.y and car.x == wall.pos:
			return True

		return False


def draw_window(win, car, walls, score):
	win.blit(BG_IMG, (0, 0))
	car.draw(win)

	for wall in walls:
		wall.draw(win)

	text = STAT_FONT.render("Score " + str(score), 1, (0, 255, 255))
	win.blit(text, (400, 20))
	pygame.display.update()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, win):
    largeText = pygame.font.Font('freesansbold.ttf',55)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIN_WIDTH/2),(WIN_HEIGHT/2))
    win.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(0.5)


def main():
	car = Car(200, 600)
	walls = [Wall(0)]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	score = 0

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		add_wall = False
		rem = []

		for wall in walls:
			wall.move()

			if wall.collide(car, wall):
				message_display('You Crashed', win)
				#pygame.quit()

			if wall.y + wall.WALL.get_width() > 1200:
				rem.append(wall)

			if wall.y > car.y + 400:
				add_wall = True

		if add_wall:
			score += 1
			walls.append(Wall(0))

		for r in rem:
			walls.remove(r)


		draw_window(win, car, walls, score)

	pygame.quit()
	quit()

main()
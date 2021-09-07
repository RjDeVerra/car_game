import pygame
import neat
import time
import os
import random
import pickle
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800

CAR_IMG = pygame.image.load("./car.png")
WALL_IMG = [pygame.image.load("./wall.jpg")]
BG_IMG = pygame.image.load("./bg.jpg")

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

	def move(self):
		self.x = 0
		 #t = [0, 200, 400]
		 #t.remove(self.x)
		 #self.x = random.choice(t)

	def move_back(self):
		self.x = 200

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

	def collide(self, car):
		if car.y == self.y and car.x == self.pos:
			return True

		return False


def draw_window(win, cars, walls, score):
	win.blit(BG_IMG, (0, 0))
	for car in cars:
		car.draw(win)

	for wall in walls:
		wall.draw(win)

	text = STAT_FONT.render("Score " + str(score), 1, (0, 255, 255))
	win.blit(text, (400, 20))
	pygame.display.update()

"""
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
"""

"""def main(genomes, config):
	nets = []
	ge = []
	cars = []

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		cars.append(Car(200, 600))
		g.fitness = 0
		ge.append(g)

	walls = [Wall(0)]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	score = 0

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
				break

		wall_ind = 0
		if len(cars) > 0:
			if len(walls) > 1 and cars[0].y > walls[0].y + walls[0].WALL.get_height():
				wall_ind = 1
		else:
			run = False
			break

		for x, car in enumerate(cars):
			ge[x].fitness += 0.1

			output = nets[cars.index(car)].activate((car.x, walls[wall_ind].pos))

			if output[0] > 0.5:
				car.move()

		add_wall = False
		rem = []

		for wall in walls:

			wall.move()

			for x, car in enumerate(cars):

				if wall.collide(car):
					#message_display('You Crashed', win)
					#pygame.quit()
					ge[x].fitness -= 1
					cars.pop(x)
					nets.pop(x)
					ge.pop(x)

			if not wall.passed and wall.y > car.y:
				wall.passed = True
				add_wall = True
				score += 1

			if wall.y > 1000:
				rem.append(wall)

		if add_wall:
			for g in ge:
				g.fitness += 5
			walls.append(Wall(0))

		for r in rem:
			walls.remove(r)
			car.move_back()


		draw_window(win, cars, walls, score)

		if score > 50:
			#pickle.dump(nets[0],open("best.pickle", "wb"))
			break"""

def main_new(genomes, config):
	cars = []
	walls = [Wall(0)]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	score = 0

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		cars.append(Car(200, 600))

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
				break

		wall_ind = 0
		if len(cars) > 0:
			if len(walls) > 1 and cars[0].y > walls[0].y + walls[0].WALL.get_height():
				wall_ind = 1
		else:
			run = False
			break

		for x, car in enumerate(cars):

			output = net.activate((car.x, walls[wall_ind].pos))

			if output[0] > 0.5:
				car.move()

		add_wall = False
		rem = []

		for wall in walls:

			wall.move()

			for x, car in enumerate(cars):

				if not wall.passed and wall.y > car.y:
					wall.passed = True
					add_wall = True
					score += 1

				if wall.y > 1000:
					rem.append(wall)

		if add_wall:
			walls.append(Wall(0))

		for r in rem:
			walls.remove(r)
			car.move_back()


		draw_window(win, cars, walls, score)



"""def run(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(main, 50)

	pickle.dump(winner,open("best.pickle", "wb"))"""

def run_with_model(config_path):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	with open('best.pickle', 'rb') as f:
		data_new = pickle.load(f)
	genomes = [(1, data_new)]

	main_new(genomes, config)

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run_with_model(config_path)
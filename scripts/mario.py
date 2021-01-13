import pygame
import sys

pygame.init()
white = (255, 255, 255)
height = 600
width = 1200
fps = 20
black = (0, 0, 0)
green = (0, 255, 0)
add_new_frame_rate = 25
cactus_img = pygame.image.load('/home/subham/Desktop/cactus.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0

fire_img = pygame.image.load('/home/subham/Desktop/fire.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mario game')

class Topscore:
	def __init__(self):
		self.high_score = 0
	def top_score(self, score):
		if score > self.high_score:
			self.high_score = score
		return self.high_score

topscore = Topscore()

class Dragon:
	dragon_velocity = 10
	def __init__(self):
		self.dragon_img = pygame.image.load('/home/subham/Desktop/dragon.png')
		self.dragon_img_rect = self.dragon_img.get_rect()
		self.dragon_img_rect.width -=10
		self.dragon_img_rect.height -= 10
		self.dragon_img_rect.top = height/2
		self.dragon_img_rect.right = width
		self.up = True
		self.down = False

	def update(self):
		canvas.blit(self.dragon_img, self.dragon_img_rect)
		if self.dragon_img_rect.top <=cactus_img_rect.bottom:
			self.up = False
			self.down = True
		elif self.dragon_img_rect.bottom>=fire_img_rect.top:
			self.up =True
			self.down = False

		if self.up:
			self.dragon_img_rect.top -=self.dragon_velocity
		elif self.down:
			self.dragon_img_rect.top+=self.dragon_velocity

class Flames:
	flames_velocity = 20

	def __init__(self):
		self.flames= pygame.image.load('/home/subham/Desktop/fireball.png')
		self.flames_img = pygame.transform.scale(self.flames,(20,20))
		self.flames_img_rect = self.flames_img.get_rect()
		self.flames_img_rect.right = dragon.dragon_img_rect.left
		self.flames_img_rect.top = dragon.dragon_img_rect.top +30

	def update(self):
		canvas.blit(self.flames_img, self.flames_img_rect)

		if self.flames_img_rect.left > 0:
			self.flames_img_rect.left-=self.flames_velocity

class Mario:
	velocity = 10
	def __init__(self):
		self.mario_img = pygame.image.load('/home/subham/Desktop/maryo.png')
		self.mario_img_rect= self.mario_img.get_rect()
		self.mario_img_rect.left =20
		self.mario_img_rect.top=height/2 -100
		self.down = True
		self.up= False

	def update(self):
		canvas.blit(self.mario_img, self.mario_img_rect)
		if self.mario_img_rect.top <= cactus_img_rect.bottom:
			gameover()
			if score> self.mario_score:
				self.mario_score= score
		if self.mario_img_rect.bottom>= fire_img_rect.top:
			gameover()
			if score > self.mario_score:
				self.mario_score = score

		if self.up:
			self.mario_img_rect.top-= 10
		if self.down:
			self.mario_img_rect.bottom+=10


def gameover():
	pygame.mixer.music.stop()
	music = pygame.mixer.sound('/home/subham/Desktop/mario_dies.wav')
	music.play()
	topscore.top_score(score)
	game_over_img = pygame.image.load('/home/subham/Desktop/end.png')
	game_over_img_rect = game_over_img.get_rect()
	game_over_img_rect.center =(width/2, height/2)
	canvas.blit(game_over_img, game_over_img_rect)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				music.stop()
				game_loop()
		pygame.display.update()

def start_game():
	canvas.fill(black)
	start_img = pygame.image.load('/home/subham/Desktop/start.png')
	start_img_rect = start_img.get_rect()
	start_img_rect.center = (width/2, height/2)
	canvas.blit(start_img, start_img_rect)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.type == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				game_loop()
		pygame.display.update()

def check_level(score):
	global level
	if score in range(0, 10):
		cactus_img_rect.bottom = 50
		fire_img_rect.top = height -50
		level =1
	elif score in range(10, 20):
		cactus_img_rect.bottom =100
		fire_img_rect.top = height-100
		level=2
	elif score in range(20, 30):
		cactus_img_rect.bottom = 150
		fire_img_rect.top= height -150
		level =3
	elif score > 30:
		cactus_img_rect.bottom =200
		fire_img_rect.top =height -200
		level = 4

def game_loop():
	while True:
		global dragon
		#dragon = Dragon
		dragon = Dragon()
		flames = Flames()
		mario = Mario()
		add_new_frame_counter =0
		global score
		score =0
		global high_score
		flames_list =[]
		pygame.mixer.music.load('/home/subham/Desktop/mario_theme.wav')
		pygame.mixer.music.play(-1, 0.0)
		while True:
			canvas.fill(black)
			check_level(score)
			dragon.update()
			add_new_frame_counter+=1

			if add_new_frame_counter == add_new_frame_rate:
				add_new_frame_counter =0
				new_flame = Flames()
				flames_list.append(new_flame)
			for f in flames_list:
				if f.flames_img_rect.left <=0:
					flames_list.remove(f)
					score +=1
				f.update()
			for event in pygame.event.get():
				if event.type== pygame.QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.flip()

if __name__ == '__main__':

	game_loop()
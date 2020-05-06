# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# sounds: dklon
# Art from Kenney.nl

import pygame
import random
from os import path
graphics_dir = path.join(path.dirname(__file__), "graphics")
sounds_dir = path.join(path.dirname(__file__), "sounds")

window_width = 1366
window_height = 768
fps = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((window_width,window_height), pygame.FULLSCREEN)
pygame.display.set_caption("Shoot'em up")
clock = pygame.time.Clock()

def load_image(image_path, scale_step):
	imported_image = pygame.image.load(path.join(graphics_dir, image_path + ".png")).convert()
	if not scale_step == (0,0):	
		imported_image = pygame.transform.scale(imported_image, scale_step)
	imported_image.set_colorkey(BLACK)
	return imported_image

class Star(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = random.choice(stars_img)
		self.size = random.randint(5, 40)
		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(self.rect.width, window_width - self.rect.width)
		self.rect.y = random.randint(-1000, -1)
		self.speedy = 0
	def update(self):
		self.speedy = self.size / 5
		self.rect.y += self.speedy
		if self.rect.top > window_height:
			self.kill()
			star = Star()
			background.add(star)

class PlayerShip(pygame.sprite.Sprite):
	def __init__(self, player_ship):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_ship
		self.rect = self.image.get_rect()
		self.radius = 32
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = window_width / 2
		self.rect.y = window_height - self.rect.height - 10
		self.health_point = 3
		self.shot_repeat = 250
		self.last_shot = pygame.time.get_ticks()
		self.lvl_damage = 3 - self.health_point
	def update(self):
		self.speedx = 0
		keyboard = pygame.key.get_pressed()
		if keyboard[pygame.K_a]:
			self.speedx = -8 
		if keyboard[pygame.K_d]:
			self.speedx = 8
		self.rect.x += self.speedx
		if self.rect.right > window_width:
			self.rect.right = window_width
		if self.rect.left < 0:
			self.rect.left = 0
		if keyboard[pygame.K_SPACE]:
			self.shoot()
	def shoot(self):
		now = pygame.time.get_ticks()

		if now - self.last_shot > self.shot_repeat:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			all_bullets.add(bullet)

def draw_health_point(surface, x, y, player_ship):
	for i in range(player_ship.health_point):
		player_ship_image = pygame.transform.scale(player_ship.image, (25,25))
		player_ship_image_rect = player_ship_image.get_rect()
		player_ship_image_rect.x = x + 30 * i
		player_ship_image_rect.y = y
		surface.blit(player_ship_image, player_ship_image_rect) 

class Meteorite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = random.choice(meteorites_img)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.87 / 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(self.rect.width, window_width - self.rect.width)
		self.rect.y = random.randrange(-300, -50)
		self.speedy = random.randrange(7, 14)
		self.speedx = random.randrange(-2, 2)
		self.center = self.rect.center
		self.respawn = True
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.respawn:
			if self.rect.top > window_height + 10 or self.rect.left < -25 or self.rect.right > window_width + 20:
				self.kill()
				meteorite = Meteorite()
				all_sprites.add(meteorite)
				all_meteorites.add(meteorite)

def new_meteorite():
	meteorite = Meteorite()
	all_sprites.add(meteorite)
	all_meteorites.add(meteorite)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		shoot_sound_1.play()
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill

class AnimatedSprite(pygame.sprite.Sprite):
	def __init__(self, images, center):
		pygame.sprite.Sprite.__init__(self)
		self.images = images
		self.frame = 0
		self.image = images[self.frame]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 60
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(self.images):
				self.kill()
			else:
				center = self.rect.center
				self.image = self.images[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

player_ship_orange_1 = load_image('player_ships\\player_ship_orange_1', (75,59))
bullet_img = load_image('bullets\\bullet_red_1', (0,0))

stars_img = []
stars_list = ['stars\\star_1','stars\\star_2','stars\\star_3']

meteorites_img = []
meteorites_list = [
'meteorites\\meteorite_big_brown_1',
'meteorites\\meteorite_big_brown_2',
'meteorites\\meteorite_big_brown_3',
'meteorites\\meteorite_big_gray_1',
'meteorites\\meteorite_big_gray_2',
'meteorites\\meteorite_big_gray_3',
'meteorites\\meteorite_med_brown_1',
'meteorites\\meteorite_med_brown_2',
'meteorites\\meteorite_med_gray_1',
'meteorites\\meteorite_med_gray_2',
'meteorites\\meteorite_small_brown_1',
'meteorites\\meteorite_small_brown_2',
'meteorites\\meteorite_small_gray_1',
'meteorites\\meteorite_small_gray_2']

explosion_anim_images_1 = []
explosion_list_1 = ['explosion_anim_1\\explosion_1','explosion_anim_1\\explosion_2',
'explosion_anim_1\\explosion_3','explosion_anim_1\\explosion_4','explosion_anim_1\\explosion_5',]

explosion_anim_images_2 = []
explosion_list_2 = ['explosion_anim_2\\explosion_1','explosion_anim_2\\explosion_2',
'explosion_anim_2\\explosion_3','explosion_anim_2\\explosion_4','explosion_anim_2\\explosion_5',]

player_ship_take_damage_anim = []
player_ship_take_damage_list = ['player_ship_take_damage_anim\\take_damage_1','player_ship_take_damage_anim\\take_damage_2','player_ship_take_damage_anim\\take_damage_3']

for player_ship_take_damage_img in player_ship_take_damage_list:
	player_ship_take_damage_anim.append(load_image(player_ship_take_damage_img, (0,0)))

for explosion_img in explosion_list_2:
	explosion_anim_images_2.append(load_image(explosion_img, (0,0)))

for explosion_img in explosion_list_1:
	explosion_anim_images_1.append(load_image(explosion_img, (0,0)))

for meteorite_img in meteorites_list:
	meteorites_img.append(load_image(meteorite_img, (0,0)))

for star_img in stars_list:
	stars_img.append(load_image(star_img, (25,25)))

explosions_animations = [explosion_anim_images_1, explosion_anim_images_2]

shoot_sound_1 = pygame.mixer.Sound(path.join(sounds_dir, 'laser_sound\\shoot_1.wav'))
pygame.mixer.music.load(path.join(sounds_dir, 'background_music\\background_1.mp3'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops= -1)

all_sprites = pygame.sprite.Group()
background = pygame.sprite.Group()
all_meteorites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

player_ship_1 = PlayerShip(player_ship_orange_1)
all_sprites.add(player_ship_1)

for star in range(60):
	star = Star()
	background.add(star)

for meteorite in range(1, 20):
	new_meteorite()

running = True
while running:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	background.update()
	all_sprites.update()

	if player_ship_1.health_point > 0:
		player_meteorite_hits = pygame.sprite.spritecollide (player_ship_1, all_meteorites, True, pygame.sprite.collide_circle)
		if player_meteorite_hits:
			player_ship_1.health_point -= 1
			new_meteorite()
			player_ship_take_damage = AnimatedSprite(player_ship_take_damage_anim, player_ship_1.rect.center)
			all_sprites.add(player_ship_take_damage)
	if player_ship_1.health_point <= 0:
		player_ship_1.kill()
		for meteorite in all_meteorites:
			meteorite.respawn = False

	player_bullet_hits = pygame.sprite.groupcollide(all_bullets, all_meteorites, True, True)
	if player_bullet_hits:
		new_meteorite()
		for hit in player_bullet_hits:
			explosion = AnimatedSprite(random.choice(explosions_animations), hit.rect.center)
			all_sprites.add(explosion)
		
	window.fill(BLACK)

	background.draw(window)
	all_sprites.draw(window)
	draw_health_point(window, 30, 30, player_ship_1)

	pygame.display.flip()
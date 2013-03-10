from pygame.sprite import Sprite
import pygame
class Blowup(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.images = [pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
							pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
							pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]
		self.image = self.images[0]
		self.pic_itr = 0
		self.is_going_on = True
	
	def update(self):
		if self.pic_itr >= 6:
			self.pic_itr = 0
			self.is_going_on = False

		self.image = self.images[self.pic_itr]
		self.pic_itr += 1
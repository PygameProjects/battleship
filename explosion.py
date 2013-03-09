from pygame.sprite import Sprite
import pygame
class Blowup(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.images = [pygame.image.load("explosion/blowup1.png"), pygame.image.load("explosion/blowup2.png"),
							pygame.image.load("explosion/blowup3.png"),pygame.image.load("explosion/blowup4.png"),
							pygame.image.load("explosion/blowup5.png"),pygame.image.load("explosion/blowup6.png")]
		self.image = self.images[0]
		self.pic_itr = 0
		self.is_going_on = True
	
	def update(self):
		if self.pic_itr >= 6:
			self.pic_itr = 0
			self.is_going_on = False

		self.image = self.images[self.pic_itr]
		self.pic_itr += 1
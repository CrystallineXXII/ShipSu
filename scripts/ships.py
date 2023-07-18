import pygame as pg
from pygame.math import Vector2
import math
from scripts.Ui import dotline

Ships = []
Bulletlist = []
def get_ship(name:str):
	for i in Ships:
		if i.name == name:
			return i
	
class Ship():

	def __init__(self, x=0, y=0,name = 'ship',color = 'white'):
		self.name = name
		self.color = color
		self.image = pg.image.load('img_assets/ship.png').convert_alpha()
		self.image = pg.transform.rotozoom(self.image, 0, 0.25)
		self.pos = Vector2(x, y)
		self.rect = self.image.get_rect(center=(x, y + 40))
		self.mask = pg.mask.from_surface(self.image)
		self.destination = Vector2(300, 300)
		self.angle = 0
		self.tempimg = None
		self.desvec = None
		self.destque = []
		self.turning = False
		self.counter = 0
		self.target = ''


		Ships.append(self)

	def shoot_at(self,target:Vector2):
		Bulletlist.append(Bullet(self.pos.copy(),target.normalize()))

	def rotate_sprite(self, sprite_image, sprite_rect, target_angle,
					  current_angle):
		# Convert angles to radians
		target_angle = math.radians(target_angle)
		current_angle = math.radians(current_angle)

		# Calculate the signed angle difference
		angle_diff = math.atan2(math.sin(target_angle - current_angle),
								math.cos(target_angle - current_angle))

		# Set the maximum angle change based on the remaining angle difference
		max_angle_change = 0.1 * angle_diff

		# Perform the angle interpolation
		interpolated_angle = current_angle + max_angle_change

		# Rotate the sprite image
		rotated_image = pg.transform.rotate(sprite_image,
											math.degrees(interpolated_angle))
		rotated_rect = rotated_image.get_rect(center=sprite_rect.center)

		return rotated_image, rotated_rect, math.degrees(interpolated_angle)

	def update(self, screen):
		if (Vector2(self.rect.centerx, self.rect.centery) -
				self.destination).magnitude() > 1:
			self.desvec = self.destination - self.pos

			self.tempimg, self.rect, self.angle = self.rotate_sprite(
				self.image, self.rect, self.desvec.angle_to(Vector2(0, -1)),
				self.angle)

			adiff = math.atan2(
				math.sin(
					math.radians(self.desvec.angle_to(Vector2(0, -1))) -
					math.radians(self.angle)),
				math.cos(
					math.radians(self.desvec.angle_to(Vector2(0, -1))) -
					math.radians(self.angle)))

			self.turning = False if math.degrees(abs(adiff)) < 5 else True
			#print(adiff)
			if not self.turning: self.pos += self.desvec.normalize() * 1
			#if not self.turning:self.pos += self.desvec.normalize() * self.desvec.magnitude() *0.05
			self.rect.center = tuple(self.pos)
			pg.draw.line(screen, 'red', tuple(self.pos),
						 tuple(self.destination))
		else:
			if any(self.destque):
				self.destination = self.destque.pop(0)
			else:
				self.tempimg, self.rect, self.angle = self.rotate_sprite(
					self.image, self.rect, 0, self.angle)
		l = [tuple(self.destination)] + [tuple(i) for i in self.destque]
		
		for i in range(len(l)-1):
			dotline(screen,l[i],l[i+1])

		for i in self.destque:
			pg.draw.circle(screen, 'lightblue', tuple(i), 5)
		
		self.mask = pg.mask.from_surface(self.tempimg)

		pg.draw.circle(screen, 'red', tuple(self.destination), 5)
		#screen.blit(self.tempimg, self.rect)
		mask = self.mask.to_surface(setcolor=self.color)
		mask.set_colorkey((0, 0, 0))
		screen.blit(mask, self.rect)

		
		if self.counter > 10:
			self.counter = 0
			enemy = get_ship(self.target)
			tvec = enemy.pos-self.pos
			if tvec.magnitude() < 250:
				self.shoot_at(tvec+enemy.desvec.normalize())
		else:
			self.counter += 1



def update_bullets(screen):
	for i in Bulletlist:
		if i.update(screen):
			Bulletlist.remove(i)
		for j in Ships:
			if j.mask.overlap(i.mask, (int(i.bpos.x - j.pos.x),
									   int(i.bpos.y - j.pos.y))):
				Bulletlist.remove(i)
				#Ships.remove(j)
				#break


class Bullet():
	
	def __init__(self,pos:Vector2,dir:Vector2):
		self.bpos = pos
		self.initpos = pos.copy()
		self.dir = dir.normalize()
		self.mask = pg.mask.from_surface(pg.surface.Surface((5,5)))
		self.mask.fill()


	def update(self,screen):
		self.bpos += self.dir * 10
		pg.draw.line(screen,'red',self.bpos,self.bpos+self.dir*7,2)
		if (self.initpos - self.bpos).magnitude() > 250:
			return True
		else:
			return False
import pygame as pg
import sys
import math
from pygame.math import Vector2

pg.init()
screen = pg.display.set_mode((1280, 800))
font = pg.font.SysFont('Monospace',40)

class Bullet():
	
	def __jnit__(self,pos:Vector2,dir:Vector2):
		self.pos = pos
		self.initpos = pos
		self.dir = dir.normalize()
		
	def update(self):
		self.pos += self.dir * 5
		if (self.initpos - self.pos).magnitude() > 100:
			return True
		else:
			return False

class Ship():

    def __init__(self, x=0, y=0):
        self.image = pg.image.load('img_assets/ship.png').convert_alpha()
        self.image = pg.transform.rotozoom(self.image, 0, 0.25)
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y + 40))
        self.destination = Vector2(300, 300)
        self.angle = 0
        self.tempimg = None
        self.desvec = None
        self.destque = []
        self.turning = False
        self.firedBullets = []

   

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

    def update(self):
        if (Vector2(self.rect.centerx, self.rect.centery) -
                self.destination).magnitude() > 5:
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
            self.rect.center = tuple(self.pos)
            pg.draw.line(screen, 'red', tuple(self.pos),tuple(self.destination))
            pg.draw.circle(screen, 'red', tuple(self.destination), 5)
        else:
            if any(self.destque):
                self.destination = self.destque.pop(0)
            else:
                self.tempimg, self.rect, self.angle = self.rotate_sprite(
                    self.image, self.rect, 0, self.angle)
        screen.blit(self.tempimg, self.rect)
        
        l = [tuple(self.destination)] + [tuple(i) for i in self.destque]
        if len(l) >= 2:
            pg.draw.lines(screen, '#222222', False, l, 2)

        for i in self.destque:
            pg.draw.circle(screen, 'lightblue', tuple(i), 5)


quitted = False
ship1 = Ship(450, 450)
ship2 = Ship(200, 200)
keypressed = False

points = [
    Vector2(300, 300),
    Vector2(300, 600),
    Vector2(600, 600),
    Vector2(600, 300)
]
ship1.destination = points[1]
mouse = (300, 300)

while not quitted:
    pg.time.Clock().tick(60)
    quitted = pg.event.get(pg.QUIT)

    screen.fill('#000010')


    if not keypressed and pg.mouse.get_pressed()[0]:
        mouse = pg.mouse.get_pos()
        ship1.destque.append(Vector2(mouse[0], mouse[1]))
        ship2.destque.append(Vector2(1280-mouse[0], 800-mouse[1]))
        keypressed = True
    elif not pg.mouse.get_pressed()[0]:
        keypressed = False

    ship1.update()
    ship2.update()
    pg.display.flip()

pg.quit()
sys.exit()

import pygame as pg
from VectorUtils import Vector2
import sys
from numpy import interp

pg.init()
screen = pg.display.set_mode((1000, 1000))


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

    def rotate_sprite(self,sprite_image, sprite_rect, target_angle, current_angle,rotation_speed):
        angle_diff = target_angle - current_angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        new_angle = current_angle + interp(angle_diff, [-180, 180], [-rotation_speed, rotation_speed])
        rotated_image = pg.transform.rotate(sprite_image, new_angle)
        rotated_rect = rotated_image.get_rect(center=sprite_rect.center)
        return rotated_image, rotated_rect, new_angle

    def update(self):
        if (Vector2(self.rect.centerx, self.rect.centery) - self.destination).magnitude > 5:
            self.desvec = self.destination - self.pos
            self.pos += self.desvec.normalized() * 1
            self.rect.center = self.pos
            self.tempimg, self.rect, self.angle = self.rotate_sprite(self.image, self.rect, self.desvec.direction, self.angle, 15)
            pg.draw.line(screen, 'red', self.pos, self.destination.intuple())
        else:
            if any(self.destque):
                self.destination = self.destque.pop(0)
            else:
                self.tempimg, self.rect, self.angle = self.rotate_sprite(self.image, self.rect,0, self.angle, 15)
        screen.blit(self.tempimg, self.rect)


quitted = False
ship = Ship(450, 450)
keypressed = False

points = [Vector2(300, 300), Vector2(300, 600), Vector2(600, 600), Vector2(600, 300)]
ship.destination = points[1]
mouse = (300, 300)

while not quitted:
    pg.time.Clock().tick(60)
    quitted = pg.event.get(pg.QUIT)

    screen.fill('#000010')

    l = [ship.destination.intuple()] + [i.intuple() for i in ship.destque]
    if len(l) >= 2:
        pg.draw.lines(screen, '#222222', False, l, 2)

    for i in ship.destque:
        pg.draw.circle(screen, 'lightblue', i.intuple(), 5)

    pg.draw.circle(screen, 'red', ship.destination.intuple(), 5)

    if not keypressed and pg.mouse.get_pressed()[0]:
        mouse = pg.mouse.get_pos()
        ship.destque.append(Vector2(mouse[0], mouse[1]))
        keypressed = True
    elif not pg.mouse.get_pressed()[0]:
        keypressed = False

    ship.update()

    pg.display.flip()

pg.quit()
sys.exit()

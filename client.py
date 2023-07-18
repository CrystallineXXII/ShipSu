import pygame as pg
from pygame.math import Vector2
pg.init()

class Shape():
    def __init__(self,x,y) -> None:
        self.pos = Vector2(x,y)
        self.color = 'green'
        self.image = pg.surface.Surface((100,100))
        pg.draw.circle(self.image,self.color,(50,50),50)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self,screen:pg.surface.Surface) -> None:

        self.rect.topleft = self.pos
        screen.blit(self.image,self.rect)
        

def move_shape(shape:Shape,screen:pg.surface.Surface):
    mouse = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0] and shape.rect.collidepoint(mouse):
        shape.pos += Vector2(pg.mouse.get_rel())
    print(pg.mouse.get_rel())
    shape.update(screen)


screen = pg.display.set_mode((1000,800))
clock = pg.time.Clock()
quitted = False

shape = Shape(100,100)

while not quitted:
    clock.tick(60)
    quitted = pg.event.get(pg.QUIT)

    screen.fill('black')
    move_shape(shape,screen)
    pg.display.flip()

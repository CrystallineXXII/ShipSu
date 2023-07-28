import pygame as pg
from pygame.math import Vector2

def dotline(screen,start:tuple[int,int],end:tuple[int,int]):
    sx = start[0]
    sy = start[1]
    ex = end[0]
    ey = end[1]

    Vec = Vector2(ex,ey) - Vector2(sx,sy)
    nVec = Vec.normalize()

    for i in range(int(Vec.magnitude()//10)):
        pg.draw.circle(screen,'#222222',tuple(Vector2(sx,sy) + nVec * 10 * i),2)


class Ui():
    def __init__(self):
        self.pos = Vector2(300,650)
        #self.uisurf = pg.surface.Surface((400,200))
    
    
    def update(self,screen:pg.surface.Surface,selection,clock,font:pg.font.Font):
        
        pg.draw.polygon(screen,'white',[
            Vector2(300,650) + Vector2(0  ,150),
            Vector2(300,650) + Vector2(100, 50),
            Vector2(300,650) + Vector2(300, 50),
            Vector2(300,650) + Vector2(400,150),
        ])


        label = font.render(f'ETA : {selection.desvec.magnitude()/(clock.get_fps()+0.01):.1f} sec(s)',1,'black')
        rect  = label.get_rect(topleft = Vector2(300,650) + Vector2(100,80))
        screen.blit(label,rect)

        label = font.render(f'<--{selection.name.upper()}-->',1,'black')
        rect  = label.get_rect(center = Vector2(300,650) + Vector2(200,70))
        screen.blit(label,rect)


        

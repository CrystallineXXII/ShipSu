import pygame as pg
from pygame.math import Vector2
import math



class Ship():

    def __init__(self, x=0, y=0,name = 'ship'):
        self.name = name
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
        screen.blit(self.tempimg, self.rect)

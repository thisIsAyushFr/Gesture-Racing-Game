import pygame
class Obstacle:
    def __init__(self):
        self.x=300
        self.y=-150
        self.height=100
        self.width=150
        self.speed=300

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def update(self,dt,screen_height):
        self.y += self.speed*dt
        self.rect.y=self.y

        if self.rect.y > screen_height:
            self.y = -self.height
            self.rect.y = self.y
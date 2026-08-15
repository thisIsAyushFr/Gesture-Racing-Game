import pygame
class Obstacle:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.height=70
        self.width=60
        self.speed=200

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def update(self,dt,screen_height):
        self.y += self.speed*dt
        self.rect.y=self.y

        if self.rect.y > screen_height:
            self.y = -self.height
            self.rect.y = self.y
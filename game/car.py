import math
import pygame
class Car:
    def __init__(self):
        self.x = 400
        self.y = 500
        self.speed = 0
        self.rotation = 0
        self.acceleration = 250
        self.max_speed = 2500
        self.drag = 0.7
        self.braking_force=500
        self.steering_strength=100

        self.rect = pygame.Rect(0,0,120,60)
        self.rect.center = (self.x,self.y)

    def update(self,dt):
        radian_rotation = math.radians(self.rotation)
        self.speed *=(self.drag**dt) #applied friction

        dx = math.cos(radian_rotation)*self.speed
        dy= math.sin(radian_rotation)*self.speed

        self.x-=dx*dt #it should be + but sprite is reversed so
        self.y-=dy*dt
        self.rect.center = (self.x,self.y)

    def accelerate(self,dt):
        self.speed +=self.acceleration*dt
        if self.speed > self.max_speed:
            self.speed =self.max_speed

    def brake(self,dt):
        if self.speed-self.braking_force*dt<0:
            self.speed=0
        else:
            self.speed-=self.braking_force*dt

    def steer(self,value,dt):
        self.rotation +=value*self.steering_strength*dt

    
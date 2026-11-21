import pygame
import random
class Obstacle:
    colors=((255,255,255),(255,120,0),(60,30,10)) #light,main,edge colours of the sprite
    lane_top=0 #road limits set by main.py
    lane_bottom=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.height=70
        self.width=60

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.build_sprite()

    def build_sprite(self):
        light,main,edge=Obstacle.colors #set by the theme
        self.sprite=pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        if random.random()<0.5:
            #striped barrier
            pygame.draw.rect(self.sprite,light,(0,0,self.width,self.height))
            for y in range(0,self.height,20):
                pygame.draw.rect(self.sprite,main,(0,y,self.width,10))
            pygame.draw.rect(self.sprite,edge,(0,0,self.width,self.height),3)
        else:
            #traffic cone seen from above
            center=(self.width//2,self.height//2)
            pygame.draw.ellipse(self.sprite,edge,(0,0,self.width,self.height))
            pygame.draw.ellipse(self.sprite,main,(4,4,self.width-8,self.height-8))
            pygame.draw.ellipse(self.sprite,light,(14,16,self.width-28,self.height-32))
            pygame.draw.circle(self.sprite,main,center,8)
        self.mask=pygame.mask.from_surface(self.sprite) #hit box follows the shape

    def update(self,dt,road_speed,screen_width,others):
        #moves with the road so it looks like it is standing on it
        self.x+=road_speed*dt
        self.rect.x=self.x

        if self.rect.x>screen_width:
            self.reset(others)
            return True #went off the right side so dodged
        return False

    def reset(self,others):
        #comes back in from the left side at a random spot on the road
        self.x=-self.width-random.randint(0,200)
        #keep at least 350px from every other obstacle so the road is never blocked
        moved=True
        while moved:
            moved=False
            for other in others:
                if other is not self and abs(other.x-self.x)<350:
                    self.x=other.x-350-random.randint(0,100)
                    moved=True
        self.y=random.randint(Obstacle.lane_top,Obstacle.lane_bottom-self.height)
        self.rect.x=self.x
        self.rect.y=self.y
        self.build_sprite() #new random look every respawn

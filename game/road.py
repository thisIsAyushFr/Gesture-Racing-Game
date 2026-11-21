import pygame
import random
from themes import shift


class RoadLine:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 150
        self.height = 8
        self.speed = 300

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )
        self.rect.centery=self.y #dash sits in the middle of y


    def update(self,dt,screen_width,strip_length):

        # move left to right
        self.x += self.speed * dt
        self.rect.x = self.x

        # reset after leaving screen
        if self.rect.left > screen_width:
            self.x -=strip_length #keeps the overshoot so gaps stay same
            self.rect.x = self.x


class Asphalt:
    def __init__(self,road,screen_width,theme):
        self.road=road
        self.width=screen_width
        self.offset=0
        self.set_theme(theme)

    def set_theme(self,theme):
        self.edge_color=theme["edge_line"]
        screen_width=self.width
        road=self.road

        #noisy tile that scrolls with the road
        self.tile=pygame.Surface((screen_width,road.height))
        self.tile.fill(theme["asphalt"])
        for i in range(12):
            patch=pygame.Rect(random.randint(0,screen_width),random.randint(0,road.height),random.randint(80,260),random.randint(20,70))
            pygame.draw.rect(self.tile,theme["asphalt_patch"],patch)
        for i in range(screen_width*road.height//60):
            x=random.randint(0,screen_width-1)
            y=random.randint(0,road.height-1)
            self.tile.set_at((x,y),shift(theme["asphalt"],random.randint(-18,22)))

    def update(self,dt,road_speed):
        self.offset=(self.offset+road_speed*dt)%self.width

    def draw(self,screen):
        screen.blit(self.tile,(self.offset,self.road.top))
        screen.blit(self.tile,(self.offset-self.width,self.road.top))
        #solid edge lines
        pygame.draw.rect(screen,self.edge_color,(0,self.road.top+6,self.width,4))
        pygame.draw.rect(screen,self.edge_color,(0,self.road.bottom-10,self.width,4))


class Curb:
    def __init__(self,road,screen_width,theme):
        self.road=road
        self.block=40
        count=screen_width//(2*self.block)+2
        self.count=count
        self.width=count*2*self.block
        self.height=14
        self.offset=0
        self.set_theme(theme)

    def set_theme(self,theme):
        #two alternating colour blocks
        self.tile=pygame.Surface((self.width,self.height))
        for i in range(self.count*2):
            if i%2==0:
                color=theme["curb_a"]
            else:
                color=theme["curb_b"]
            pygame.draw.rect(self.tile,color,(i*self.block,0,self.block,self.height))

    def update(self,dt,road_speed):
        self.offset=(self.offset+road_speed*dt)%self.width

    def draw(self,screen):
        for y in (self.road.top-self.height,self.road.bottom):
            screen.blit(self.tile,(self.offset,y))
            screen.blit(self.tile,(self.offset-self.width,y))


class SpeedLines:
    def __init__(self,road,screen_width,count=14):
        self.road=road
        self.screen_width=screen_width
        self.lines=[] #each line is [x,y]
        for i in range(count):
            self.lines.append([random.randint(0,screen_width),random.randint(road.top+14,road.bottom-14)])

    def update(self,dt,road_speed):
        for line in self.lines:
            line[0]+=road_speed*1.6*dt
            if line[0]-300>self.screen_width:
                line[0]=-random.randint(0,200)
                line[1]=random.randint(self.road.top+14,self.road.bottom-14)

    def draw(self,screen,ratio,color):
        if ratio<0.15:
            return #no lines at low speed
        length=int(30+ratio*150)
        strength=0.4+0.6*ratio
        line_color=(int(color[0]*strength),int(color[1]*strength),int(color[2]*strength))
        for line in self.lines:
            pygame.draw.line(screen,line_color,(line[0]-length,line[1]),(line[0],line[1]),2)

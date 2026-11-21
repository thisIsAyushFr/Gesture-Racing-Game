import pygame
import random

class Background:
    def __init__(self,screen_width,screen_height,road,theme):
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.road=road
        self.set_theme(theme)

    def set_theme(self,theme):
        road=self.road
        width=self.screen_width
        self.layers=[] #each layer is [surface,x offset,speed factor,y,width]

        #night gradient or sky made once
        self.gradient=pygame.Surface((width,self.screen_height))
        top=theme["sky_top"]
        bottom=theme["sky_bottom"]
        for y in range(self.screen_height):
            t=y/self.screen_height
            color=(int(top[0]+(bottom[0]-top[0])*t),int(top[1]+(bottom[1]-top[1])*t),int(top[2]+(bottom[2]-top[2])*t))
            pygame.draw.line(self.gradient,color,(0,y),(width,y))

        top_space=road.top-30
        bottom_space=self.screen_height-road.bottom-30
        #ground colour beside the road for the day themes
        if theme["ground"]:
            ground_top=int(top_space*0.6)
            ground_bottom=int(bottom_space*0.6)
            pygame.draw.rect(self.gradient,theme["ground"],(0,road.top-30-ground_top,width,ground_top+30))
            pygame.draw.rect(self.gradient,theme["ground"],(0,road.bottom,width,ground_bottom+30))

        if theme["scenery"] in ("city","neon"):
            far_ratio=0.9
            near_ratio=0.5
        else:
            far_ratio=0.45
            near_ratio=0.3
        #far layer first then near layer so near ones draw on top
        self.add_objects(theme,top_space,road.top-30,False,far_ratio,theme["far_color"],0.3,0)
        self.add_objects(theme,bottom_space,road.bottom+30,True,far_ratio,theme["far_color"],0.3,0)
        self.add_objects(theme,top_space,road.top-30,False,near_ratio,theme["near_color"],0.6,1)
        self.add_objects(theme,bottom_space,road.bottom+30,True,near_ratio,theme["near_color"],0.6,1)
        if theme["lights"]:
            self.add_lights(theme)

    def add_objects(self,theme,space,base_y,hanging_down,height_ratio,color,factor,layer):
        width=self.screen_width
        height=int(space*height_ratio)
        surf=pygame.Surface((width,height),pygame.SRCALPHA)
        kind=theme["scenery"]
        if kind=="city" or kind=="neon":
            self.draw_buildings(surf,width,height,color,theme,kind=="neon")
        elif kind=="desert":
            if layer==0:
                self.draw_rocks(surf,width,height,color)
            else:
                self.draw_cacti(surf,width,height,color)
        elif kind=="forest":
            self.draw_trees(surf,width,height,color)
        else:
            self.draw_pines(surf,width,height,color)

        if hanging_down:
            surf=pygame.transform.flip(surf,False,True)
            y=base_y
        else:
            y=base_y-height
        self.layers.append([surf,0,factor,y,width])

    def draw_buildings(self,surf,width,height,color,theme,neon):
        x=0
        while x<width:
            building_width=random.randint(50,130)
            if x+building_width>width:
                building_width=width-x #last one fills the gap so the strip tiles
            building_height=random.randint(height//3,height)
            top=height-building_height
            pygame.draw.rect(surf,color,(x,top,building_width,building_height))
            if neon:
                pygame.draw.rect(surf,theme["accent"],(x,top,building_width,building_height),2)
            #lit windows
            for window_y in range(top+8,height-8,16):
                for window_x in range(x+8,x+building_width-8,14):
                    if random.random()<0.35:
                        pygame.draw.rect(surf,theme["window"],(window_x,window_y,5,7))
            x+=building_width+random.randint(0,6)

    def draw_rocks(self,surf,width,height,color):
        x=0
        while x<width-140:
            rock_width=random.randint(height//2,height)
            rock_height=random.randint(height//4,height//2)
            pygame.draw.ellipse(surf,color,(x,height-rock_height,rock_width,rock_height))
            x+=rock_width+random.randint(30,140)

    def draw_cacti(self,surf,width,height,color):
        x=0
        while x<width-100:
            cactus_height=random.randint(height//2,height)
            pygame.draw.rect(surf,color,(x+14,height-cactus_height,14,cactus_height),border_radius=6)
            arm_y=height-cactus_height+cactus_height//3
            pygame.draw.rect(surf,color,(x,arm_y,28,8),border_radius=4) #left arm
            pygame.draw.rect(surf,color,(x,arm_y-18,8,26),border_radius=4)
            pygame.draw.rect(surf,color,(x+14,arm_y+14,28,8),border_radius=4) #right arm
            pygame.draw.rect(surf,color,(x+34,arm_y-4,8,26),border_radius=4)
            x+=random.randint(110,260)

    def draw_trees(self,surf,width,height,color):
        x=0
        while x<width-100:
            tree_height=random.randint(height//2,height)
            radius=int(tree_height*0.35)
            trunk_height=int(tree_height*0.35)
            pygame.draw.rect(surf,(90,60,30),(x+radius-4,height-trunk_height,8,trunk_height))
            pygame.draw.circle(surf,color,(x+radius,height-trunk_height-radius+6),radius)
            pygame.draw.circle(surf,color,(x+radius-radius//2,height-trunk_height),radius//2+4)
            pygame.draw.circle(surf,color,(x+radius+radius//2,height-trunk_height),radius//2+4)
            x+=radius*2+random.randint(10,70)

    def draw_pines(self,surf,width,height,color):
        x=0
        while x<width-100:
            pine_height=random.randint(height//2,height)
            pine_width=int(pine_height*0.55)
            middle=x+pine_width//2
            for i in range(3):
                #three stacked triangles each a bit smaller
                top=height-pine_height+i*(pine_height//4)
                bottom=top+pine_height//2
                half=pine_width//2-i*(pine_width//8)
                pygame.draw.polygon(surf,color,[(middle,top),(middle-half,bottom),(middle+half,bottom)])
                pygame.draw.polygon(surf,(245,248,255),[(middle,top),(middle-half//2,top+(bottom-top)//2),(middle+half//2,top+(bottom-top)//2)])
            x+=pine_width+random.randint(10,60)

    def add_lights(self,theme):
        road=self.road
        count=self.screen_width//300+1
        spacing=300
        width=count*spacing
        glow=theme["accent"]
        surf=pygame.Surface((width,30),pygame.SRCALPHA)
        for i in range(count):
            x=i*spacing+spacing//2
            pygame.draw.circle(surf,(glow[0],glow[1],glow[2],40),(x,15),14)
            pygame.draw.circle(surf,(glow[0],glow[1],glow[2],80),(x,15),8)
            pygame.draw.circle(surf,(255,255,235),(x,15),4)
        self.layers.append([surf,0,1.0,road.top-44,width])
        self.layers.append([surf,0,1.0,road.bottom+14,width])

    def update(self,dt,road_speed):
        for layer in self.layers:
            layer[1]=(layer[1]+road_speed*layer[2]*dt)%layer[4]

    def draw(self,screen):
        screen.blit(self.gradient,(0,0))
        for layer in self.layers:
            screen.blit(layer[0],(layer[1],layer[3]))
            screen.blit(layer[0],(layer[1]-layer[4],layer[3]))

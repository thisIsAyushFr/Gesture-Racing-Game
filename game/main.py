import os
import sys
import pygame
import cv2
from car import Car
from obstacles import Obstacle
from road import RoadLine,Asphalt,Curb,SpeedLines
from scenery import Background
from themes import THEMES
from hand_tracker import HandTracker
from gestures import fingers_up,action_detection,steer_value,hand_calibration

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH=os.path.join(BASE_DIR,"..","images","car1.png")
START_LIVES=3
START_OBSTACLES=3
MAX_OBSTACLES=10

def spawn_obstacle(others):
    obstacle=Obstacle(0,0)
    obstacle.reset(others) #placed away from the others
    return obstacle

def make_obstacles(count):
    obstacles=[]
    for i in range(count):
        obstacles.append(spawn_obstacle(obstacles))
    return obstacles

def reset_car(car,screen_width,screen_height):
    car.speed=0
    car.rotation=0
    car.x=screen_width-300
    car.y=(screen_height-165)/2

def main():
    pygame.init()
    fps_clock=pygame.time.Clock()
    screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen_width=screen.get_width()
    screen_height=screen.get_height()
    pygame.display.set_caption("Gesture Racing Game")

    road_height=250
    road=pygame.Rect(0,(screen_height-road_height)//2,screen_width,road_height)
    #150 dash + 50 gap, enough dashes for the screen plus 2 extra
    line_spacing=200
    line_count=screen_width//line_spacing+3
    strip_length=line_count*line_spacing
    road_lines=[]
    for i in range(line_count):
        road_lines.append(RoadLine(-line_spacing+i*line_spacing,road.centery))

    theme_index=0
    theme=THEMES[theme_index]
    Obstacle.colors=theme["obstacle"]
    Obstacle.lane_top=road.top+20 #stay between the edge lines
    Obstacle.lane_bottom=road.bottom-20
    background=Background(screen_width,screen_height,road,theme)
    asphalt=Asphalt(road,screen_width,theme)
    curb=Curb(road,screen_width,theme)
    speed_lines=SpeedLines(road,screen_width)

    car=Car()
    reset_car(car,screen_width,screen_height)
    obstacles=make_obstacles(START_OBSTACLES)
    car_image=pygame.image.load(IMAGE_PATH)
    resized_car_image=pygame.transform.scale(car_image,(150,80))

    font=pygame.font.Font(None,40)
    big_font=pygame.font.Font(None,90)
    no_hand_text=font.render("No hand detected - please reposition your hand",True,(255,255,255))
    no_hand_rect=no_hand_text.get_rect(center=(screen_width//2,screen_height//2))
    no_hand_box=no_hand_rect.inflate(40,30)
    small_font=pygame.font.Font(None,28)
    calibrate_text=font.render("Press C to calibrate",True,theme["hud"])

    tracker=HandTracker()
    camera=cv2.VideoCapture(0)
    if not camera.isOpened():
        pygame.quit()
        sys.exit("Could not open the webcam")

    calibrated=False
    score=0
    lives=START_LIVES
    game_over=False
    landmarks=[]
    preview=None
    show_preview=True
    running=True

    while running:
        dt=fps_clock.tick(60)/1000

        success,frame=camera.read()
        if success:
            frame=cv2.flip(frame,1)
            frame,landmarks=tracker.frame_processing(frame)
            #small camera view for the corner
            small_frame=cv2.resize(frame,(240,180))
            small_frame=cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
            preview=pygame.image.frombuffer(small_frame.tobytes(),(240,180),"RGB")
        else:
            landmarks=[] #failed read counts as no hand
            preview=None

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False
                elif event.key==pygame.K_c and landmarks:
                    hand_calibration(landmarks)
                    calibrated=True
                elif event.key==pygame.K_t:
                    theme_index=(theme_index+1)%len(THEMES)
                    theme=THEMES[theme_index]
                    Obstacle.colors=theme["obstacle"]
                    background.set_theme(theme)
                    asphalt.set_theme(theme)
                    curb.set_theme(theme)
                    for obstacle in obstacles:
                        obstacle.build_sprite() #new colours straight away
                    calibrate_text=font.render("Press C to calibrate",True,theme["hud"])
                elif event.key==pygame.K_v:
                    show_preview=not show_preview
                elif event.key==pygame.K_r and game_over:
                    score=0
                    lives=START_LIVES
                    game_over=False
                    obstacles=make_obstacles(START_OBSTACLES)
                    reset_car(car,screen_width,screen_height)

        if not game_over:
            if landmarks:
                fingers=fingers_up(landmarks)
                action=action_detection(fingers)
                steering=steer_value(landmarks)
                if action=="ACCELERATE":
                    car.accelerate(dt)
                elif action=="BRAKE":
                    car.brake(dt)
                car.steer(steering,dt)
            else:
                car.brake(dt) #no hand so brake

            car.update(dt)

            #clamp using only the visible pixels of the rotated car
            rotated_car=pygame.transform.rotate(resized_car_image,-car.rotation)
            car_rect=rotated_car.get_rect(center=(car.x,car.y))
            visible_rect=rotated_car.get_bounding_rect()
            visible_rect.x+=car_rect.x
            visible_rect.y+=car_rect.y

            if visible_rect.top<road.top:
                car.y+=road.top-visible_rect.top
            if visible_rect.bottom>road.bottom:
                car.y-=visible_rect.bottom-road.bottom
            #endless road: leaving one side puts the car on the other side like a new page
            new_page=False
            if visible_rect.right<0:
                car.x+=screen_width-visible_rect.left
                new_page=True
            elif visible_rect.left>screen_width:
                car.x-=visible_rect.right
                new_page=True
            if new_page:
                obstacles=make_obstacles(len(obstacles))

            car_rect.center=(car.x,car.y)
            car.rect=car_rect
            car_mask=pygame.mask.from_surface(rotated_car)

            #road moves faster when the car is faster
            road_speed=100+car.speed*0.5

            for obstacle in obstacles:
                if obstacle.update(dt,road_speed,screen_width,obstacles): #true only when it left the right side
                    score+=1
            #more obstacles as the score goes up
            while len(obstacles)<min(START_OBSTACLES+score//5,MAX_OBSTACLES):
                obstacles.append(spawn_obstacle(obstacles))

            for line in road_lines:
                line.speed=road_speed
                line.update(dt,screen_width,strip_length)
            background.update(dt,road_speed)
            asphalt.update(dt,road_speed)
            curb.update(dt,road_speed)
            speed_lines.update(dt,road_speed)

            for obstacle in obstacles:
                if car_rect.colliderect(obstacle.rect):
                    offset=(obstacle.rect.x-car_rect.x,obstacle.rect.y-car_rect.y)
                    if car_mask.overlap(obstacle.mask,offset):
                        car.speed=0
                        obstacle.reset(obstacles)
                        lives-=1
                        if lives<=0:
                            game_over=True
        else:
            rotated_car=pygame.transform.rotate(resized_car_image,-car.rotation)
            car_rect=rotated_car.get_rect(center=(car.x,car.y))

        background.draw(screen)
        asphalt.draw(screen)
        curb.draw(screen)
        for line in road_lines:
            pygame.draw.rect(screen,theme["dash"],line.rect)
        speed_lines.draw(screen,min(car.speed/car.max_speed,1),theme["speed_line"])
        screen.blit(rotated_car,car_rect.topleft)
        for obstacle in obstacles:
            screen.blit(obstacle.sprite,obstacle.rect.topleft)

        if show_preview and preview:
            screen.blit(preview,(screen_width-260,20))
            pygame.draw.rect(screen,(255,255,255),(screen_width-260,20,240,180),2)

        screen.blit(font.render("Score: "+str(score),True,theme["hud"]),(20,20))
        screen.blit(font.render("Lives: "+str(lives),True,theme["hud"]),(20,60))
        screen.blit(small_font.render("Theme: "+theme["name"]+" (T)   Camera (V)",True,theme["hud"]),(20,screen_height-40))
        if not calibrated:
            screen.blit(calibrate_text,(20,100))

        if game_over:
            title=big_font.render("GAME OVER",True,(255,255,255))
            sub=font.render("Score: "+str(score)+"   R - restart   ESC - quit",True,(255,255,255))
            title_rect=title.get_rect(center=(screen_width//2,screen_height//2-30))
            sub_rect=sub.get_rect(center=(screen_width//2,screen_height//2+40))
            box=title_rect.union(sub_rect).inflate(60,40)
            pygame.draw.rect(screen,(0,0,0),box)
            pygame.draw.rect(screen,(255,255,255),box,2)
            screen.blit(title,title_rect)
            screen.blit(sub,sub_rect)
        elif not landmarks:
            pygame.draw.rect(screen,(0,0,0),no_hand_box)
            pygame.draw.rect(screen,(255,255,255),no_hand_box,2)
            screen.blit(no_hand_text,no_hand_rect)

        pygame.display.update()

    camera.release()
    pygame.quit()

main()

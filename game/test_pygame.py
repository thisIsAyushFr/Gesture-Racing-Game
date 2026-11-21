import pygame
from car import Car
from obstacles import Obstacle
import cv2
from hand_tracker import HandTracker
from road import RoadLine
from gestures import (
    fingers_up,
    action_detection,
    steer_value,
    hand_calibration,
)


pygame.init()
fps_clock = pygame.time.Clock()
width = 800
height = 600

car = Car()
obstacles = [
    Obstacle(300,-200),
    Obstacle(600,-500),
    Obstacle(200,-800),
    Obstacle(700,-1100),
    Obstacle(400,-1400)
]



screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((800,600))
screen_width = screen.get_width()
screen_height = screen.get_height()

road_width = screen_width
road_height = 250

road = pygame.Rect(
    0,
    (screen_height - road_height)//2,
    road_width,
    road_height
)
#150 dash + 50 gap, enough dashes for the screen plus 2 extra
line_spacing=200
line_count=screen_width//line_spacing+3
strip_length=line_count*line_spacing
road_lines=[]
for i in range(line_count):
    road_lines.append(RoadLine(-line_spacing+i*line_spacing,road.centery))


print(screen_width, screen_height)
pygame.display.set_caption("Game")

car.x = screen_width-300
car.y = (screen_height-165)/2

car_image = pygame.image.load("images/car1.png")
resized_car_image = pygame.transform.scale(car_image,(150, 80))

font = pygame.font.Font(None,40)
calibrated=False
score=0
no_hand_text=font.render("No hand detected - please reposition your hand",True,(255,255,255))
no_hand_rect=no_hand_text.get_rect(center=(screen_width//2,screen_height//2))
no_hand_box=no_hand_rect.inflate(40,30)
calibrate_text=font.render("Press C to calibrate",True,(0,0,0))

tracker = HandTracker()
camera = cv2.VideoCapture(0)
running = True
while running:
    dt = fps_clock.tick(60)
    dt = dt/1000

    success,frame = camera.read()
    frame = cv2.flip(frame,1)
    frame,landmarks = tracker.frame_processing(frame)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type==pygame.KEYDOWN:
            if i.key == pygame.K_c and landmarks:
                hand_calibration(landmarks)
                calibrated=True
                print("caliberated")

    #cv2.imshow("Cam",frame)
    if landmarks:
        fingers=fingers_up(landmarks)
        action=action_detection(fingers)
        steering=steer_value(landmarks)
        if action == "ACCELERATE":
            car.accelerate(dt)
        elif action == "BRAKE":
           car.brake(dt)
        car.steer(steering,dt)
    else:
        car.brake(dt) #no hand so brake


    car.update(dt)

    #clamp using only the visible pixels of the rotated car
    rotated_car = pygame.transform.rotate(resized_car_image,-car.rotation)
    car_rect = rotated_car.get_rect(center=(car.x,car.y))
    visible_rect = rotated_car.get_bounding_rect()
    visible_rect.x +=car_rect.x
    visible_rect.y +=car_rect.y

    if visible_rect.top < road.top:
        car.y +=road.top-visible_rect.top
    if visible_rect.bottom > road.bottom:
        car.y -=visible_rect.bottom-road.bottom
    if visible_rect.left < 0:
        car.x -=visible_rect.left
    if visible_rect.right > screen_width:
        car.x -=visible_rect.right-screen_width

    car_rect.center = (car.x,car.y)
    car.rect = car_rect
    car_mask = pygame.mask.from_surface(rotated_car)

    for obstacle in obstacles:
        if obstacle.update(dt,screen_width,screen_height): #true only when it left the bottom
            score +=1

    for line in road_lines:
        line.update(dt,screen_width,strip_length)
        

    for obstacle in obstacles:
        if car_rect.colliderect(obstacle.rect):
            offset = (obstacle.rect.x-car_rect.x,obstacle.rect.y-car_rect.y)
            if car_mask.overlap(obstacle.mask,offset):
                print("COLLISION")
                car.speed=0
                obstacle.reset(screen_width)

    screen.fill((255,255,255))
    pygame.draw.rect(screen,(50,50,50),road)
    for line in road_lines:
        pygame.draw.rect(screen,(255,255,255),line.rect)
    screen.blit(rotated_car,car_rect.topleft)
    #green outline is the real collision shape
    outline_points=[]
    for point in car_mask.outline():
        outline_points.append((point[0]+car_rect.x,point[1]+car_rect.y))
    if len(outline_points)>1:
        pygame.draw.lines(screen,(0,255,0),True,outline_points,2)
    for obstacle in obstacles:
        pygame.draw.rect(screen,(255,0,0),obstacle.rect)
    score_text=font.render("Score: "+str(score),True,(0,0,0))
    screen.blit(score_text,(20,20))
    if not calibrated:
        screen.blit(calibrate_text,(20,60)) #below the score
    #popup only while hand is lost
    if not landmarks:
        pygame.draw.rect(screen,(0,0,0),no_hand_box)
        pygame.draw.rect(screen,(255,255,255),no_hand_box,2)
        screen.blit(no_hand_text,no_hand_rect)
    pygame.display.update()
    
pygame.quit()
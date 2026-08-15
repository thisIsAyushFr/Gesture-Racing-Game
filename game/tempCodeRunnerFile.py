import pygame
from car import Car
from obstacles import Obstacle
import cv2
from hand_tracker import HandTracker
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
obstacles= [Obstacle(),Obstacle(),Obstacle(),Obstacle(),Obstacle()]

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((800,600))
screen_width = screen.get_width()
screen_height = screen.get_height()

print(screen_width, screen_height)
pygame.display.set_caption("Game")

car.x = screen_width-300
car.y = (screen_height-165)/2

car_image = pygame.image.load("images/car1.png")
resized_car_image = pygame.transform.scale(car_image,(150, 80))

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


    car.update(dt)
    for obstacle in obstacles:
        obstacle.update(dt,screen_height)

    for obstacle in obstacles:
        if car.rect.colliderect(obstacle.rect):
            print("COLLISION")
            car.speed=0
            obstacle.y=-obstacle.height
            obstacle.rect.y=obstacle.y

    screen.fill((255,255,255))
    rotated_car = pygame.transform.rotate(resized_car_image,-car.rotation)
    car_rect = rotated_car.get_rect(center=(car.x,car.y))
    screen.blit(rotated_car,car_rect.topleft)
    pygame.draw.rect(screen,(0,255,0),car.rect,2)
    for obstacle in obstacles:
        pygame.draw.rect(screen,(255,0,0),obstacle.rect)
    pygame.display.update()
    
pygame.quit()
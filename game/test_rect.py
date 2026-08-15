import pygame
pygame.init()

width=100
height=50
x=100
y=150

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()

rect = pygame.Rect(screen_width//2,screen_height//2,width,height)

running=True

while running:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            running=False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                running = False
    screen.fill((255,255,255))
    rect.x+=2
    pygame.draw.rect(screen,(255,0,0),rect,2)
    pygame.display.update()

pygame.quit()
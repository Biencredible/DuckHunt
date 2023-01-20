import pygame
import math

pygame.init()
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 32)
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
backgrounds = []
banners = []
guns = []
level = 1
banner_top = HEIGHT - 200

for level_index in range(1, 4):
    backgrounds.append(pygame.image.load(f'assets/bgs/{level_index}.png')) #f for formatted string because a variable is needed. Access variable with {level_index}
    banners.append(pygame.image.load(f'assets/banners/{level_index}.png'))
    guns.append(pygame.image.load(f'assets/guns/{level_index}.png'))

#main loop
run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(backgrounds[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, banner_top))

    #if level > 0:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()



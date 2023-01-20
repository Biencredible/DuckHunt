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
level = 3
banner_top = HEIGHT - 200

for level_index in range(1, 4):
    backgrounds.append(pygame.image.load(f'assets/bgs/{level_index}.png')) #f for formatted string because a variable is needed. Access variable with {level_index}
    banners.append(pygame.image.load(f'assets/banners/{level_index}.png'))
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{level_index}.png'), (100, 100)))

def draw_gun():
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (WIDTH/2, banner_top)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()
    if mouse_pos[0] != gun_point[0]:
        slope = (mouse_pos[1] - gun_point[1])/(mouse_pos[0] - gun_point[0])
    else:
        slope = -100000 #large negative number is approx straight line
    angle = math.atan(slope)
    rotation = math.degrees(angle)
    if mouse_pos[0] < WIDTH/2:
        gun = pygame.transform.flip(guns[level - 1], True, False)
        if mouse_pos[1] < banner_top:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH/2 - 90, HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level -1], mouse_pos, 5)
    else:
        gun = guns[level -1]
        if mouse_pos[1] < banner_top:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH/2 - 30, HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level -1], mouse_pos, 5)


#main loop
run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(backgrounds[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, banner_top))

    if level > 0:
        draw_gun()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()



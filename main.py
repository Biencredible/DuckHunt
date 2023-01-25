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
target_images = [[], [], []]
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}
level = 3
banner_top = HEIGHT - 200

for level_index in range(1, 4):
    backgrounds.append(pygame.image.load(f'assets/bgs/{level_index}.png')) #f for formatted string because a variable is needed. Access variable with {level_index}
    banners.append(pygame.image.load(f'assets/banners/{level_index}.png'))
    guns.append(pygame.transform.scale(pygame.image.load(f'assets/guns/{level_index}.png'), (100, 100)))
    if level_index < 3:
        for target_index in range(1, 4):
            target_images[level_index - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{level_index}/{target_index}.png'),
                                    (120 - (target_index*18), 80 - (target_index*12))))
    else:
        for target_index in range(1, 5):
            target_images[level_index - 1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{level_index}/{target_index}.png'),
                                    (120 - (target_index*18), 80 - (target_index*12))))

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


def draw_level(coordinates):
    if level == 1 or level == 2:
        target_rects = [[], [], []]
    else:
        target_rects = [[], [], [], []]
    for tier_index in range(len(coordinates)):
        for start_position_index in range(len(coordinates[tier_index])):
            target_rects[tier_index].append(pygame.rect.Rect((coordinates[tier_index][start_position_index][0] + 20,
                                                              coordinates[tier_index][start_position_index][1]),
                                                              (60 - tier_index * 12, 60 - tier_index * 12)))
            screen.blit(target_images[level - 1][tier_index], coordinates[tier_index][start_position_index])
    return target_rects


#initialize enemy coordinates
one_coordinates = [[], [], []]
two_coordinates = [[], [], []]
three_coordinates = [[], [], [], []]
for tier_index in range(3):
    temporary_target_list = targets[1]
    for start_position_index in range(temporary_target_list[tier_index]):
        one_coordinates[tier_index].append((WIDTH//(temporary_target_list[tier_index]) * start_position_index, #// -> floor devision
                                            300 - (tier_index * 150) + 30 * (start_position_index % 2))) # alternate in adding 30
for tier_index in range(3):
    temporary_target_list = targets[2]
    for start_position_index in range(temporary_target_list[tier_index]):
        two_coordinates[tier_index].append((WIDTH//(temporary_target_list[tier_index]) * start_position_index, #// -> floor devision
                                            300 - (tier_index * 150) + 30 * (start_position_index % 2))) # alternate in adding 30
for tier_index in range(4):
    temporary_target_list = targets[3]
    for start_position_index in range(temporary_target_list[tier_index]):
        three_coordinates[tier_index].append((WIDTH // (temporary_target_list[tier_index]) * start_position_index,  # // -> floor devision
                                            300 - (tier_index * 100) + 30 * (start_position_index % 2)))  # alternate in adding 30


#main loop
run = True
while run:
    timer.tick(fps)

    screen.fill('black')
    screen.blit(backgrounds[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, banner_top))

    if level == 1:
        target_boxes = draw_level(one_coordinates)
    elif level == 2:
        target_boxes = draw_level(two_coordinates)
    elif level == 3:
        target_boxes = draw_level(three_coordinates)

    if level > 0:
        draw_gun()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()



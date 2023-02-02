import pygame
import math

pygame.init()
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 32)
big_font = pygame.font.Font('assets/font/myFont.ttf', 60)
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
level = 1
points = 0
total_shots = 0
mode = 0
# 0 = freeplay, 1 = accuracy, 2 = timed
ammo = 0
time_passed = 0
time_remaining = 0
counter = 1
best_freeplay = 0
best_ammo = 0
best_time = 0
shot = False
menu = True
game_over = False
pause = False
clicked = False
write_values = False
new_coords = True
banner_top = HEIGHT - 200
menu_img = pygame.image.load(f'assets/menus/mainMenu.png')
game_over_img = pygame.image.load(f'assets/menus/gameOver.png')
pause_img = pygame.image.load(f'assets/menus/pause.png')


for level_index in range(1, 4):
    # f for formatted string because a variable is needed. Access variable with {level_index}
    backgrounds.append(pygame.image.load(f'assets/bgs/{level_index}.png'))
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


file = open('high_scores.txt', 'r')
read_file = file.readlines()
file.close()
best_freeplay = int(read_file[0])
best_ammo = int(read_file[1])
best_time = int(read_file[2])


def draw_score():
    points_text = font.render(f'Points: {points}', True, 'black')
    screen.blit(points_text, (320, 660))
    shots_text = font.render(f'Total Shots: {total_shots}', True, 'black')
    screen.blit(shots_text, (320, 687))
    time_text = font.render(f'Time Elapsed: {time_passed}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == 0:
        mode_text = font.render(f'Freeplay!', True, 'black')
    elif mode == 1:
        mode_text = font.render(f'Ammo Remaing: {ammo}', True, 'black')
    if mode == 2:
        mode_text = font.render(f'Time Remaining: {time_remaining}', True, 'black')
    screen.blit(mode_text, (320, 741))


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


def move_level(coordinates):
    if level == 1 or level == 2:
        max_tier = 3
    else:
        max_tier = 4
    for tier_index in range(max_tier):
        for start_position_index in range(len(coordinates[tier_index])):
            temporary_coords = coordinates[tier_index][start_position_index]
            if temporary_coords[0] < -150:
                coordinates[tier_index][start_position_index] = WIDTH, temporary_coords[1]
            else:
                coordinates[tier_index][start_position_index] = (temporary_coords[0] - 2**tier_index, temporary_coords[1])
    return coordinates


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


def check_shot(targets, coordinates):
    global points
    mouse_pos = pygame.mouse.get_pos()
    for tier_index in range(len(targets)):
        for target_index in range(len(targets[tier_index])):
            if targets[tier_index][target_index].collidepoint(mouse_pos):
                coordinates[tier_index].pop(target_index)
                points += 10 + 10 * (tier_index**2)
                # add sounds for enemy hit
    return coordinates


def draw_menu():
    global game_over, pause, mode, level, menu, time_passed, total_shots, points, ammo, time_remaining
    global best_freeplay, best_ammo, best_time, write_values, clicked, new_coords
    game_over = False
    pause = False
    screen.blit(menu_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    freeplay_button = pygame.rect.Rect((170, 524), (260, 100))
    screen.blit(font.render(f'{best_freeplay}', True, 'black'), (340, 580))
    ammo_button = pygame.rect.Rect((475, 524), (260, 100))
    screen.blit(font.render(f'{best_ammo}', True, 'black'), (650, 580))
    timed_button = pygame.rect.Rect((170, 661), (260, 100))
    screen.blit(font.render(f'{best_time}', True, 'black'), (350, 710))
    reset_button = pygame.rect.Rect((475, 661), (260, 100))
    if freeplay_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 0
        level = 1
        menu = False
        time_passed = 0
        total_shots = 0
        points = 0
        clicked = True
        new_coords = True
    if ammo_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 1
        level = 1
        menu = False
        time_passed = 0
        total_shots = 0
        points = 0
        ammo = 81
        clicked = True
        new_coords = True
    if timed_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        mode = 2
        level = 1
        menu = False
        time_passed = 0
        total_shots = 0
        points = 0
        time_remaining = 30
        clicked = True
        new_coords = True
    if reset_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        best_freeplay = 0
        best_ammo = 0
        best_time = 0
        clicked = True
        write_values = True


def draw_game_over():
    global level, pause, menu, points, total_shots, total_shots, time_passed, time_remaining, clicked
    if mode == 0:
        display_score = time_passed
    else:
        display_score = points
    screen.blit(game_over_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    exit_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))
    screen.blit(big_font.render(f'{display_score}', True, 'black'), (650, 570))
    if menu_button.collidepoint(mouse_pos) and clicks [0] and not clicked:
        level = 0
        pause = False
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        time_remaining = 0
        clicked = True
    if exit_button.collidepoint(mouse_pos) and clicks [0] and not clicked:
        global run
        run = False


def draw_pause():
    global level, pause, menu, points, total_shots, total_shots, time_passed, time_remaining, clicked, new_coords
    screen.blit(pause_img, (0,0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    resume_button = pygame.rect.Rect((170, 661), (260, 100))
    menu_button = pygame.rect.Rect((475, 661), (260, 100))
    if resume_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = resume_level
        pause = False
    if menu_button.collidepoint(mouse_pos) and clicks[0] and not clicked:
        level = 0
        pause = False
        menu = True
        points = 0
        total_shots = 0
        time_passed = 0
        time_remaining = 0
        clicked = True
        new_coords = True


def initialize_enemy_coordinates():
    global one_coordinates, two_coordinates, three_coordinates
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
    if level != 0:
        if counter < 60:
            counter += 1
        else:
            counter = 1
            time_passed += 1
            if mode == 2:
                time_remaining -= 1

    if new_coords:
        initialize_enemy_coordinates()
        new_coords = False

    screen.fill('black')
    screen.blit(backgrounds[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, banner_top))

    if menu:
        level = 0
        draw_menu()
    if game_over:
        level = 0
        draw_game_over()
    if pause:
        level = 0
        draw_pause()

    if level == 1:
        target_boxes = draw_level(one_coordinates)
        one_coordinates = move_level(one_coordinates)
        if shot:
            one_coordinates = check_shot(target_boxes, one_coordinates)
            shot = False
    elif level == 2:
        target_boxes = draw_level(two_coordinates)
        two_coordinates = move_level(two_coordinates)
        if shot:
            two_coordinates = check_shot(target_boxes, two_coordinates)
            shot = False
    elif level == 3:
        target_boxes = draw_level(three_coordinates)
        three_coordinates = move_level(three_coordinates)
        if shot:
            three_coordinates = check_shot(target_boxes, three_coordinates)
            shot = False

    if level > 0:
        draw_gun()
        draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            if(0 < mouse_position[0] < WIDTH) and (0 < mouse_position[1] < banner_top):
                shot = True
                total_shots += 1
                if mode == 1:
                    ammo -= 1
            if (670 < mouse_position[0] < 860) and (660 < mouse_position[1] < 715):
                resume_level = level
                pause = True
                clicked = True
            if (670 < mouse_position[0] < 860) and (715 < mouse_position[1] < 760):
                menu = True
                clicked = True
                new_coords = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and clicked:
            clicked = False

    if level > 0:
        if target_boxes == [[], [], []] and level < 3:
            level += 1
        if (level == 3 and target_boxes == [[], [], [], []]) or (mode == 1 and ammo == 0) or (mode == 2 and time_remaining == 0):
            new_coords = True
            if mode == 0:
                if time_passed < best_freeplay or best_freeplay == 0:
                    best_freeplay = time_passed
                    write_values = True
            if mode == 1:
                if points > best_ammo:
                    best_ammo = points
                    write_values = True
            if mode == 2:
                if points > best_time:
                    best_time = points
                    write_values = True
            game_over = True
    if write_values:
        file = open('high_scores.txt', 'w')
        file.write(f'{best_freeplay}\n{best_ammo}\n{best_time}')

    pygame.display.flip()

pygame.quit()



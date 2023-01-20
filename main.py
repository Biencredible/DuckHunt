import pygame
import math

pygame.init()
fps = 60
time = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 32)
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
backgrounds = []
banners = []
guns = []
level = 0

for level_index in range(1, 4):
    backgrounds.append(pygame.image.load(f'assets/bgs/{level_index}.png')) #f for formatted string because a variable is needed. Access variable with {level_index}
    banners.append(pygame.image.load(f'assets/banners/{level_index}.png'))
    guns.append(pygame.image.load(f'assets/guns/{level_index}.png'))

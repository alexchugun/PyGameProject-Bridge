import pygame
from settings import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

background_image = pygame.image.load('assets/images/background.png')

is_running = True

while is_running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

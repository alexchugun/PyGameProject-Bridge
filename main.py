import pygame
from settings import *
from utils import *
from player import Player
from world import World

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Строитель мостов")
clock = pygame.time.Clock()

background_image = pygame.image.load('assets/images/background.png')

is_running = True
is_drawing_bridge = False
is_falling_bridge = False

world_data = [
    [2, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]

world = World(world_data)
player = Player(0, 650, world.tile_list)
h = 0

while is_running:
    screen.blit(background_image, (0, 0))

    world.draw(screen)
    player.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_drawing_bridge = True
                is_falling_bridge = False
                x, y = player.rect.x, player.rect.y
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                is_drawing_bridge = False
                is_falling_bridge = True
                h1 = h
                h = 0
                a = 0

    if is_drawing_bridge:
        pygame.draw.line(screen, 'black',
                         [(player.rect.x + player.image_width) // 2, player.rect.y + player.image_height],
                         [(player.rect.x + player.image_width) // 2, player.rect.y - h], 5)
        h += 3

    if is_falling_bridge:
        if a <= 90:
            x_ = h1 * sin_grad(a)
            y_ = h1 * cos_grad(a)
            pygame.draw.line(screen, 'black',
                             [(player.rect.x + player.image_width) // 2, player.rect.y + player.image_height],
                             [(player.rect.x + player.image_width) // 2 + x_, player.rect.y + player.image_height - y_],
                             5)
            a += 1

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

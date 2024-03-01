import pprint

import pygame
from settings import *
from utils import *
from player import Player
from world import World
from bridge import Bridge

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Строитель мостов")
clock = pygame.time.Clock()

background_image = pygame.image.load('assets/images/background.png')

is_running = True
is_drawing_bridge = False
is_falling_bridge = False
screen_scroll = 0

world_data = [
    [2, 2, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
]

world = World()
world.set_data(world_data)
player = Player(50, 650, world.tile_list)
h = 0

bridge_group = pygame.sprite.Group()

while is_running:
    screen.blit(background_image, (0, 0))

    world.draw(screen, screen_scroll)
    screen_scroll = player.update(screen, bridge_group)

    bridge_group.update(screen_scroll)
    bridge_group.draw(screen)

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
                angle = 0

    if is_drawing_bridge:
        pygame.draw.line(screen, 'black',
                         [player.rect.centerx, player.rect.y + player.image_height],
                         [player.rect.centerx, player.rect.y - h], 5)
        h += 3

    if is_falling_bridge:
        if angle <= 90:
            x_ = h1 * sin_grad(angle)
            y_ = h1 * cos_grad(angle)
            pygame.draw.line(screen, 'black',
                             [player.rect.centerx, player.rect.y + player.image_height],
                             [player.rect.centerx + x_, player.rect.y + player.image_height - y_],
                             5)
            angle += 1
        else:
            is_falling_bridge = False
            angle = 0

            bridge_start = player.rect.centerx
            bridge_end = h1

            # проверка надо ли пройти больше. ПОКА НЕ РАБОТАЕТ!!!
            for tile in world.tile_list:
                if tile[1].x < player.rect.x:
                    continue
                if bridge_end > tile[1].x + TILE_SIZE:
                    h1 += player.image_width
                    break
                if tile[1].x + TILE_SIZE >= SCREEN_WIDTH - SCROLL_THRESHOLD + bridge_end >= tile[1].x:
                    break

            new_bridge = Bridge(player.rect.centerx, bridge_end)
            bridge_group.add(new_bridge)

            player.is_moving = True
            dx = 0

    if player.is_moving:
        if dx <= h1:  # + player.image_width
            dx += VELOCITY
        else:
            player.is_moving = False

            # dx = 0
            # while dx <= h1:
            #     player.rect.x += 1
            #     dx += 1

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

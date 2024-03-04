import pprint

import pygame
from settings import *
from utils import *
from player import Player
from world import World
from bridge import Bridge
from button import Button


def restart_level():
    bridge_group.empty()
    world.set_data(world_data)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Строитель мостов")
clock = pygame.time.Clock()

background_image = pygame.image.load('assets/images/background.png')
screen_saver_image = pygame.image.load('assets/images/screen_saver.png')
start_btn_image = pygame.image.load('assets/images/play_btn.png')
exit_btn_image = pygame.image.load('assets/images/exit_btn.png')
restart_btn_image = pygame.image.load('assets/images/restart_btn.png')

is_running = True
is_drawing_bridge = False
is_falling_bridge = False
is_start_game = False
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
player = Player(51, 650, world.tile_list)
h = 0

start_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 250, start_btn_image, 1)
exit_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, exit_btn_image, 1)
restart_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, restart_btn_image, 1)

bridge_group = pygame.sprite.Group()

while is_running:
    if not is_start_game:
        screen.blit(screen_saver_image, (0, 0))

        if start_btn.draw(screen):
            is_start_game = True

        if exit_btn.draw(screen):
            is_running = False
    else:
        if player.is_alive:
            screen.blit(background_image, (0, 0))

            world.draw(screen, screen_scroll)
            screen_scroll = player.update(screen, bridge_group)

            bridge_group.update(screen_scroll)
            bridge_group.draw(screen)

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

                    is_tile_match_bridge = False

                    for i in range(len(world.tile_list) - 1):
                        # print(world.tile_list[i])

                        # если земля до игрока то пропускаем
                        if world.tile_list[i][1].x < player.rect.x:
                            continue

                        # # проверка что мост длиннее земли
                        # if bridge_start + bridge_end > world.tile_list[i][1].x + TILE_SIZE and world.tile_list[i][1].x + TILE_SIZE != world.tile_list[i + 1][1].x:
                        #     print(bridge_start + bridge_end, world.tile_list[i][1].x + TILE_SIZE)
                        #     h1 += player.image_width
                        #     is_bridge_longer_tile = True
                        #     break

                        if world.tile_list[i][1].x + TILE_SIZE >= bridge_start + bridge_end >= world.tile_list[i][1].x:
                            is_tile_match_bridge = True
                            break

                        # if world.tile_list[i][1].x + TILE_SIZE >= SCREEN_WIDTH - SCROLL_THRESHOLD + bridge_end >= world.tile_list[i][1].x:
                        #     break

                    print('----------------------------------------------------------------')

                    if not is_tile_match_bridge:
                        h1 += player.image_width

                    new_bridge = Bridge(player.rect.centerx, bridge_end)
                    bridge_group.add(new_bridge)

                    player.is_moving = True
                    dx = 0

            if player.is_moving:
                if dx <= h1:  # + player.image_width
                    dx += VELOCITY
                else:
                    player.is_moving = False
        else:
            screen_scroll = 0

            if restart_btn.draw(screen):
                restart_level()
                player = Player(51, 650, world.tile_list)

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

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

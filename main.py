import pprint

import pygame
from pygame import mixer
from settings import *
from utils import *
from player import Player
from world import World
from bridge import Bridge
from button import Button
import csv


def restart_level():
    bridge_group.empty()
    world.set_data(world_data)


def draw_text(text, t_x, t_y, text_size=40):
    font = pygame.font.SysFont('Arial', text_size)
    t = font.render(text, True, (255, 255, 255))
    screen.blit(t, (t_x, t_y))


mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Строитель мостов")
clock = pygame.time.Clock()

background_image = pygame.image.load('assets/images/background.png')
screen_saver_image = pygame.image.load('assets/images/screen_saver.png')
start_btn_image = pygame.image.load('assets/images/play_btn.png')
exit_btn_image = pygame.image.load('assets/images/exit_btn.png')
restart_btn_image = pygame.image.load('assets/images/restart_btn.png')

pygame.mixer.music.load('assets/audio/background.mp3')
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 0.0, 3000)
bridge_build_sound = pygame.mixer.Sound('assets/audio/bridge_build.mp3')
bridge_build_sound.set_volume(0.5)
bridge_falling_sound = pygame.mixer.Sound('assets/audio/bridge_falling.mp3')
bridge_falling_sound.set_volume(1)
game_over_sound = pygame.mixer.Sound('assets/audio/game_over.mp3')
game_over_sound.set_volume(1)

is_running = True
is_drawing_bridge = False
is_falling_bridge = False
is_start_game = False
screen_scroll = 0
score = 0
level = 1

world_data = []
for row in range(ROWS):
    r = [0] * COLS
    world_data.append(r)

with open(f'levels/level{level}.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
exit = world.set_data(world_data)
player = Player(51, 650, world.tile_list)
h = 0

start_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 250, start_btn_image, 1)
exit_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, exit_btn_image, 1)
restart_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, restart_btn_image, 1)

bridge_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

exit_group.add(exit)

while is_running:
    if not is_start_game:
        screen.blit(screen_saver_image, (0, 0))

        draw_text('Добро пожаловать в игру Строитель мостов!', 150, 800)
        draw_text('Управление: пробел - строить мост, -> - двигаться', 150, 850)

        if start_btn.draw(screen):
            is_start_game = True

        if exit_btn.draw(screen):
            is_running = False
    else:
        if player.is_alive:
            screen.blit(background_image, (0, 0))

            world.draw(screen, screen_scroll)
            screen_scroll, level_complete = player.update(screen, bridge_group, exit_group)
            print(level_complete)

            bridge_group.update(screen_scroll)
            bridge_group.draw(screen)

            exit_group.update(screen_scroll)
            exit_group.draw(screen)

            draw_text(f'Очки: {score}', 10, 10)

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

                        if world.tile_list[i][1].x + TILE_SIZE >= bridge_start + bridge_end >= world.tile_list[i][1].x:
                            is_tile_match_bridge = True
                            break

                    if not is_tile_match_bridge:
                        h1 += player.image_width
                    else:
                        score += 1

                    new_bridge = Bridge(player.rect.centerx, bridge_end)
                    bridge_group.add(new_bridge)

                    player.is_moving = True
                    dx = 0

            if player.is_moving:
                if dx <= h1:
                    dx += VELOCITY
                else:
                    player.is_moving = False
        else:
            screen_scroll = 0
            draw_text('Вы погибли!', 400, 420)
            # game_over_sound.play(1)

            if restart_btn.draw(screen):
                restart_level()
                player = Player(51, 650, world.tile_list)
                score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_drawing_bridge = True
                is_falling_bridge = False
                x, y = player.rect.x, player.rect.y
                bridge_build_sound.play(30)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                is_drawing_bridge = False
                is_falling_bridge = True
                h1 = h
                h = 0
                angle = 0
                bridge_build_sound.stop()
                bridge_falling_sound.play()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

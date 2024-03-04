from typing import Tuple, List, Any

import pygame.transform
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_list):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.index = 0
        self.count = 0

        for i in range(1, 3):
            player_image = pygame.image.load(f'assets/images/player{i}.png')
            player_image = pygame.transform.scale(player_image, (40, 40))
            self.images.append(player_image)

        self.player_image = self.images[self.index]
        self.rect = self.player_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image_width = self.player_image.get_width()
        self.image_height = self.player_image.get_height()
        self.velocity_y = 0
        self.dy = 0
        self.tile_list = tile_list
        self.is_moving = False
        self.is_alive = True

    def update(self, screen, bridge_group, exit_group) -> tuple[int, bool]:
        screen_scroll = 0
        dx = 0
        self.dy = 0

        if self.is_moving:
            dx += VELOCITY
            self.count += 1
        else:
            key = pygame.key.get_pressed()

            if key[pygame.K_RIGHT]:
                dx += VELOCITY
                self.count += 1
            else:
                self.count = 0
                self.index = 0
                self.player_image = self.images[self.index]

        if self.count > WALKING_COOLDOWN:
            self.count = 0
            self.index += 1
            self.index %= 2
            self.player_image = self.images[self.index]

        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.dy += self.velocity_y

        level_complete = self.check_collision(bridge_group, exit_group)
        self.check_is_falling()

        self.rect.x += dx
        self.rect.y += self.dy

        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESHOLD:
            self.rect.x -= dx
            screen_scroll = -dx

        screen.blit(self.player_image, self.rect)

        return screen_scroll, level_complete

    def check_collision(self, bridge_group, exit_group):
        for tile in self.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, 1, self.image_height):
                if self.velocity_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.velocity_y = 0

        if pygame.sprite.spritecollide(self, bridge_group, False):
            self.dy = 0

        if pygame.sprite.spritecollide(self, exit_group, False):
            return True
        else:
            return False

    def check_is_falling(self):
        if self.rect.bottom > SCREEN_HEIGHT:
            self.is_alive = False

import pygame.transform
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_list):
        pygame.sprite.Sprite.__init__(self)
        player_image = pygame.image.load('assets/images/player.png')
        self.player_image = pygame.transform.scale(player_image, (40, 40))
        self.rect = self.player_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image_width = self.player_image.get_width()
        self.image_height = self.player_image.get_height()
        self.velocity_y = 0
        self.dy = 0
        self.tile_list = tile_list

    def update(self, screen, bridge_group) -> int:
        screen_scroll = 0
        dx = 0
        self.dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx -= VELOCITY
        if key[pygame.K_RIGHT]:
            dx += VELOCITY

        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.dy += self.velocity_y

        self.check_collision(bridge_group)

        self.rect.x += dx
        self.rect.y += self.dy

        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESHOLD:
            self.rect.x -= dx
            screen_scroll = -dx

        screen.blit(self.player_image, self.rect)

        return screen_scroll

    def check_collision(self, bridge_group):
        for tile in self.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.image_width, self.image_height):
                if self.velocity_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.velocity_y = 0

        if pygame.sprite.spritecollide(self, bridge_group, False):
            self.dy = 0

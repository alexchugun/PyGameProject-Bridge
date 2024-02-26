import pygame.transform
from settings import *


class Player:
    def __init__(self, x, y):
        player_image = pygame.image.load('assets/images/player.png')
        self.player_image = pygame.transform.scale(player_image, (40, 40))
        self.rect = self.player_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image_width = self.player_image.get_width()
        self.image_height = self.player_image.get_height()

    def update(self, screen):
        dx = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx -= VELOCITY
        if key[pygame.K_RIGHT]:
            dx += VELOCITY

        self.rect.x += dx

        screen.blit(self.player_image, self.rect)

import pygame.sprite
from settings import *


class Bridge(pygame.sprite.Sprite):
    def __init__(self, x_start, width):
        pygame.sprite.Sprite.__init__(self)
        self.x_start = x_start
        image = pygame.image.load('assets/images/bridge.png')
        self.image = pygame.transform.scale(image, (width, 15))

        self.rect = self.image.get_rect()
        self.rect.x = self.x_start
        self.rect.y = SCREEN_HEIGHT - 5 * TILE_SIZE - 5
        self.rect.width = width

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

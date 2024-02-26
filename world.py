import pygame.image
from settings import *


class World:
    def __init__(self):
        self.tile_list = []
        self.ground_img = pygame.image.load('assets/images/ground.png')
        self.grass_img = pygame.image.load('assets/images/grass.png')

    def set_data(self, data):
        self.tile_list.clear()
        row_count = 15
        for row in data:
            for col_count, col in enumerate(row):
                if col == 1:
                    img = pygame.transform.scale(self.ground_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if col == 2:
                    img = pygame.transform.scale(self.grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

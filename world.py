import pygame.image
from settings import *
from exit import Exit


class World:
    def __init__(self):
        self.tile_list = []
        self.ground_img = pygame.image.load('assets/images/ground.png')
        self.grass_img = pygame.image.load('assets/images/grass.png')
        self.exit_img = pygame.image.load('assets/images/exit.png')

    def set_data(self, data):
        self.tile_list.clear()
        row_count = 14
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
                if col == 3:
                    img = pygame.transform.scale(self.exit_img, (TILE_SIZE, TILE_SIZE))
                    exit = Exit(img, col_count * TILE_SIZE, row_count * TILE_SIZE)

            row_count += 1

        return exit

    def draw(self, screen, screen_scroll):
        for tile in self.tile_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])

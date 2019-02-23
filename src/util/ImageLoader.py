import pygame as pygame

from util import Constants


class ImageLoader:

    def __init__(self):

        self.image_map = {}
        self.PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\"

    def load(self, tile_code):

        if tile_code not in self.image_map.keys():
            self.image_map[tile_code] = pygame.image.load(self.PATH + str(tile_code))

        return self.image_map[tile_code]



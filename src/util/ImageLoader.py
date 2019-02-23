import pygame as pygame

from util import Constants


class ImageLoader:

    def __init__(self):

        self.image_map = {}
        self.PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\"

    def load(self, tile_code):

        if tile_code not in self.image_map.keys():
            picture = pygame.image.load(self.PATH + str(tile_code) + ".png")
            picture.convert()

            self.image_map[tile_code] = pygame.transform.scale(picture, (Constants.TILE_SIZE, Constants.TILE_SIZE))

        return self.image_map[tile_code]



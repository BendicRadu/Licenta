import pygame as pygame

from util import Constants


class ImageLoader:

    def __init__(self):

        self.image_map = {}
        self.PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\"
        self.player_images = []

    def init_player_images(self):

        down = pygame.image.load(self.PATH + "\\player\\0.png")
        down.convert()
        down = pygame.transform.scale(down, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        up = pygame.image.load(self.PATH + "\\player\\1.png")
        up.convert()
        up = pygame.transform.scale(up, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        left = pygame.image.load(self.PATH + "\\player\\2.png")
        left.convert()
        left = pygame.transform.scale(left, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        right = pygame.image.load(self.PATH + "\\player\\3.png")
        right.convert()
        right = pygame.transform.scale(right, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        self.player_images.append(down)
        self.player_images.append(up)
        self.player_images.append(left)
        self.player_images.append(right)

    def load(self, tile_code):

        if tile_code not in self.image_map.keys():
            picture = pygame.image.load(self.PATH + str(tile_code) + ".png")
            picture.convert()

            self.image_map[tile_code] = pygame.transform.scale(picture, (Constants.TILE_SIZE, Constants.TILE_SIZE))

        return self.image_map[tile_code]


    def load_player_image(self, direction):

        if len(self.player_images) == 0:
            self.init_player_images()

        return self.player_images[direction.value]

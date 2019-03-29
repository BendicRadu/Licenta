import pygame as pygame

from util import Constants


class ImageLoader:

    def __init__(self):

        self.world_image_map = {}
        self.inventory_image_map = {}
        self.crafting_image_map = {}

        self.WORLD_IMAGE_PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\world\\"
        self.UI_IMAGE_PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\ui\\"
        self.PLAYER_IMAGE_PATH = "C:\\Licenta\\Licenta\\resources\\Sprites\\player\\"

        self.player_images = []

        self.ui_background = None
        self.required_items_background = None

    def pygame_init(self):
        self.init_player_images()
        self.init_ui()
        self.init_required_items_background()

    def init_player_images(self):
        down = pygame.image.load(self.PLAYER_IMAGE_PATH + "0.png")
        down.convert()
        down = pygame.transform.scale(down, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        up = pygame.image.load(self.PLAYER_IMAGE_PATH + "1.png")
        up.convert()
        up = pygame.transform.scale(up, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        left = pygame.image.load(self.PLAYER_IMAGE_PATH + "2.png")
        left.convert()
        left = pygame.transform.scale(left, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        right = pygame.image.load(self.PLAYER_IMAGE_PATH + "3.png")
        right.convert()
        right = pygame.transform.scale(right, (Constants.PLAYER_SIZE, Constants.PLAYER_SIZE))

        self.player_images.append(down)
        self.player_images.append(up)
        self.player_images.append(left)
        self.player_images.append(right)

    def init_ui(self):
        ui_background = pygame.image.load(self.UI_IMAGE_PATH + "ui_background.png")
        ui_background.convert()
        ui_background = pygame.transform.scale(ui_background, (Constants.UI_WIDTH, Constants.UI_HEIGHT))

        self.ui_background = ui_background

    def init_required_items_background(self):

        picture = pygame.image.load(self.UI_IMAGE_PATH + "-1.png")
        picture = pygame.transform.scale(picture, (
            Constants.REQUIRED_ITEMS_SCREEN_WIDTH, Constants.REQUIRED_ITEMS_SCREEN_HEIGHT))
        picture.convert()

        surface = pygame.Surface((Constants.REQUIRED_ITEMS_SCREEN_WIDTH, Constants.REQUIRED_ITEMS_SCREEN_HEIGHT))
        surface.blit(picture, picture.get_rect())

        self.required_items_background = surface

    # =======LOADER======================================================================================================

    def load_world_image(self, tile_code):
        if tile_code not in self.world_image_map.keys():
            picture = pygame.image.load(self.WORLD_IMAGE_PATH + str(tile_code) + ".png")
            picture.convert()
            picture = pygame.transform.scale(picture, (Constants.TILE_SIZE, Constants.TILE_SIZE))

            surface = pygame.Surface((Constants.TILE_SIZE, Constants.TILE_SIZE))
            surface.blit(picture, picture.get_rect())

            self.world_image_map[tile_code] = surface

        return self.world_image_map[tile_code]

    def load_player_image(self, direction):
        return self.player_images[direction.value]

    def load_inventory_image(self, tile_code):

        if tile_code not in self.inventory_image_map.keys():
            picture = pygame.image.load(self.UI_IMAGE_PATH + str(tile_code) + ".png")
            picture = pygame.transform.scale(picture, (Constants.INVENTORY_CELL_SIZE, Constants.INVENTORY_CELL_SIZE))
            picture.convert()

            surface = pygame.Surface((Constants.INVENTORY_CELL_SIZE, Constants.INVENTORY_CELL_SIZE))
            surface.blit(picture, picture.get_rect())

            self.inventory_image_map[tile_code] = surface

        return self.inventory_image_map[tile_code]

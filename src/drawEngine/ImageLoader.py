import pygame as pygame

from util import GameVars
from util.GameVars import BASE_PATH


class ImageLoader:

    def __init__(self):

        self.world_image_map = {}
        self.inventory_image_map = {}
        self.crafting_image_map = {}

        self.WORLD_IMAGE_PATH = BASE_PATH + "resources\\Sprites\\world\\"
        self.UI_IMAGE_PATH = BASE_PATH + "resources\\Sprites\\ui\\"
        self.PLAYER_IMAGE_PATH = BASE_PATH + "resources\\Sprites\\player\\"

        self.player_images = []

        self.ui_background = None
        self.required_items_background = None
        self.non_visible_tile = None

    def pygame_init(self):
        self.init_player_images()
        self.init_ui()
        self.init_required_items_background()
        self.init_non_visible_tile()

    def init_non_visible_tile(self):
        surface = pygame.Surface((GameVars.TILE_SIZE, GameVars.TILE_SIZE))
        surface.fill((0, 0, 0), surface.get_rect())

        self.non_visible_tile = surface

    def init_player_images(self):
        down = pygame.image.load(self.PLAYER_IMAGE_PATH + "0.png")
        down.convert()
        down = pygame.transform.scale(down, (GameVars.PLAYER_SIZE, GameVars.PLAYER_SIZE))

        up = pygame.image.load(self.PLAYER_IMAGE_PATH + "1.png")
        up.convert()
        up = pygame.transform.scale(up, (GameVars.PLAYER_SIZE, GameVars.PLAYER_SIZE))

        left = pygame.image.load(self.PLAYER_IMAGE_PATH + "2.png")
        left.convert()
        left = pygame.transform.scale(left, (GameVars.PLAYER_SIZE, GameVars.PLAYER_SIZE))

        right = pygame.image.load(self.PLAYER_IMAGE_PATH + "3.png")
        right.convert()
        right = pygame.transform.scale(right, (GameVars.PLAYER_SIZE, GameVars.PLAYER_SIZE))

        self.player_images.append(down)
        self.player_images.append(up)
        self.player_images.append(left)
        self.player_images.append(right)

    def init_ui(self):
        ui_background = pygame.image.load(self.UI_IMAGE_PATH + "ui_background.png")
        ui_background.convert()
        ui_background = pygame.transform.scale(ui_background, (GameVars.UI_WIDTH, GameVars.UI_HEIGHT))

        self.ui_background = ui_background

    def init_required_items_background(self):

        picture = pygame.image.load(self.UI_IMAGE_PATH + "-1.png")
        picture = pygame.transform.scale(picture, (GameVars.REQUIRED_ITEMS_SCREEN_WIDTH, GameVars.REQUIRED_ITEMS_SCREEN_HEIGHT))
        picture.convert()

        surface = pygame.Surface((GameVars.REQUIRED_ITEMS_SCREEN_WIDTH, GameVars.REQUIRED_ITEMS_SCREEN_HEIGHT))
        surface.blit(picture, picture.get_rect())

        self.required_items_background = surface

    # =======LOADER======================================================================================================

    def load_world_image(self, tile_code):
        if tile_code not in self.world_image_map.keys():
            picture = pygame.image.load(self.WORLD_IMAGE_PATH + str(tile_code) + ".png")
            picture.convert()
            picture = pygame.transform.scale(picture, (GameVars.TILE_SIZE, GameVars.TILE_SIZE))

            surface = pygame.Surface((GameVars.TILE_SIZE, GameVars.TILE_SIZE))
            surface.blit(picture, picture.get_rect())

            self.world_image_map[tile_code] = surface

        return self.world_image_map[tile_code]

    def load_player_image(self, direction):
        return self.player_images[direction.value]

    def load_inventory_image(self, tile_code):

        if tile_code not in self.inventory_image_map.keys():
            picture = pygame.image.load(self.UI_IMAGE_PATH + str(tile_code) + ".png")
            picture = pygame.transform.scale(picture, (GameVars.INVENTORY_CELL_SIZE, GameVars.INVENTORY_CELL_SIZE))
            picture.convert()

            surface = pygame.Surface((GameVars.INVENTORY_CELL_SIZE, GameVars.INVENTORY_CELL_SIZE))
            surface.blit(picture, picture.get_rect())

            self.inventory_image_map[tile_code] = surface

        return self.inventory_image_map[tile_code]

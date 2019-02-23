import pygame

from maps.ScreenMap.ScreenMap import ScreenMap
from sprites.Player import Player
from sprites.MapSprite import Sprite
from sprites.Tile import SelectedTile
from util import Constants


class RenderMap:

    def __init__(self):

        # TODO Save chunk offset and pos on a file
        self.screen_map = ScreenMap()

        self.sprite_list = []

        # TODO Player coords should also be saved in a file
        self.player = Player(500 * Constants.TILE_SIZE, 500 * Constants.TILE_SIZE)

        self.camera = Camera()

    def get_sprites(self):

        tile_matrix = self.screen_map.get_tiles()

        self.sprite_list = []

        for i in range(len(tile_matrix.matrix)):
            for j in range(len(tile_matrix.matrix[0])):
                tile_code = tile_matrix.matrix[i][j]

                x = j * Constants.TILE_SIZE - self.camera.offset_x
                y = i * Constants.TILE_SIZE - self.camera.offset_y

                sprite = Sprite(x, y, tile_code)

                self.sprite_list.append(sprite)

        return self.sprite_list

    def move_player(self, direction):

        if self.validate_direction(direction):
            self.screen_map.move_player(direction)
            self.camera.move_camera(direction)

    def validate_direction(self, direction):

        cam_x, cam_y = self.camera.mock_move(direction)

        tile_top_left = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y,
            cam_x, cam_y
        )

        tile_bottom_right = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X + Constants.PLAYER_SIZE // 2,
            Constants.PLAYER_SCREEN_Y + Constants.PLAYER_SIZE // 2,
            cam_x, cam_y
        )

        player_rect_top_left = pygame.Rect(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y,
            Constants.PLAYER_SIZE, Constants.PLAYER_SIZE
        )

        player_rect_bottom_right = pygame.Rect(
            Constants.PLAYER_SCREEN_X + Constants.PLAYER_SIZE // 2,
            Constants.PLAYER_SCREEN_Y + Constants.PLAYER_SIZE // 2,
            10, 10
        )

        tile_rect_top_left = self.to_rect(tile_top_left, cam_x, cam_y)
        tile_rect_bottom_right = self.to_rect(tile_bottom_right, cam_x, cam_y)

        # Check if the top and bottom corners collide (Since the tile starts from top-left)

        if int(tile_top_left.tile_code) in Constants.TILES_WITH_COLLIDERS:
            if player_rect_top_left.colliderect(tile_rect_top_left) \
                    or player_rect_bottom_right.colliderect(tile_rect_top_left):
                return False

        # Check collision with tile underneath

        if int(tile_bottom_right.tile_code) in Constants.TILES_WITH_COLLIDERS:
            if player_rect_bottom_right.colliderect(tile_rect_bottom_right)\
                    or player_rect_top_left.colliderect(tile_rect_top_left):
                return False

        return True

    def to_rect(self, tile, cam_x, cam_y):

        x = tile.j * Constants.TILE_SIZE - cam_x
        y = tile.i * Constants.TILE_SIZE - cam_y

        return pygame.Rect(x, y, Constants.TILE_SIZE, Constants.TILE_SIZE)

    def get_selected_tile(self, mouse_pos_raw):

        mouse_pos_x = mouse_pos_raw[0] + self.camera.offset_x
        mouse_pos_y = mouse_pos_raw[1] + self.camera.offset_y

        tile = self.screen_map.get_selected_tile((mouse_pos_x, mouse_pos_y))

        x = tile.j * Constants.TILE_SIZE - self.camera.offset_x
        y = tile.i * Constants.TILE_SIZE - self.camera.offset_y

        return SelectedTile(x, y, tile.tile_code)


class Camera:

    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def move_camera(self, direction):
        self.offset_x += direction[0]
        self.offset_y += direction[1]

        self.offset_x %= Constants.TILE_SIZE
        self.offset_y %= Constants.TILE_SIZE

    def mock_move(self, direction):
        x = self.offset_x
        y = self.offset_y

        x += direction[0]
        y += direction[1]

        # x %= Constants.TILE_SIZE
        # y %= Constants.TILE_SIZE

        return x, y

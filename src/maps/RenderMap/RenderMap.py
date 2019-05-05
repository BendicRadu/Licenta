import pygame

from maps.ScreenMap.ScreenMap import ScreenMap
from sprites.Player import Player
from sprites.MapSprite import Sprite
from sprites.Tile import SelectedTile
from util import Constants
from util.Constants import Direction
from util.Singleton import Singleton


class RenderMap:

    def __init__(self):

        # TODO Save chunk offset and pos on a file
        self.screen_map = ScreenMap()

        self.sprite_list = []

        # TODO Player coords should also be saved in a file

        self.player = Singleton.player

        self.camera = Camera()

    def get_camera_coords(self):
        return self.camera.offset_x, self.camera.offset_y

    def get_player_coords(self):
        return self.player.global_x, self.player.global_y

    def get_chunk_offset(self):
        return self.screen_map.get_chunk_offset()

    def get_chunk_pos(self):
        return self.screen_map.get_chunk_pos()

    def re_apply_effects(self):
        self.screen_map.apply_effects()

    # If the player is on a mover tile, get the speed vector
    def get_player_auto_move(self):

        tile_under_player = self.get_tile_under_player().tile_code

        if tile_under_player not in Constants.TILES_MOVERS_DIRECTIONS.keys():
            return None

        direction = Constants.TILES_MOVERS_DIRECTIONS[tile_under_player]
        speed     = Constants.TILES_MOVERS_SPEEDS[tile_under_player]

        direction_vector = Direction.get_direction_vector(direction)
        speed_vector = direction_vector[0] * speed, direction_vector[1] * speed

        return speed_vector


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

        # TODO Refactor

        tile_top_left = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y,
            cam_x, cam_y
        )

        tile_top_right = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X + Constants.PLAYER_SIZE,
            Constants.PLAYER_SCREEN_Y,
            cam_x, cam_y
        )

        tile_bottom_left = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y + Constants.PLAYER_SIZE,
            cam_x, cam_y
        )

        tile_bottom_right = self.screen_map.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X + Constants.PLAYER_SIZE,
            Constants.PLAYER_SCREEN_Y + Constants.PLAYER_SIZE,
            cam_x, cam_y
        )

        player_rect = pygame.Rect(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y,
            Constants.PLAYER_SIZE, Constants.PLAYER_SIZE
        )

        tile_rect_top_left = self.to_rect(tile_top_left, cam_x, cam_y)
        tile_rect_top_right = self.to_rect(tile_top_right, cam_x, cam_y)
        tile_rect_bottom_right = self.to_rect(tile_bottom_right, cam_x, cam_y)
        tile_rect_bottom_left = self.to_rect(tile_bottom_left, cam_x, cam_y)

        # Check if the top and bottom corners collide (Since the tile starts from top-left)

        if tile_top_left.tile_code in Constants.TILES_WITH_COLLIDERS:
            if player_rect.colliderect(tile_rect_top_left):
                return False

        if tile_bottom_right.tile_code in Constants.TILES_WITH_COLLIDERS:
            if player_rect.colliderect(tile_rect_bottom_right):
                return False


        if tile_top_right.tile_code in Constants.TILES_WITH_COLLIDERS:
            if player_rect.colliderect(tile_rect_top_right):
                return False

        if tile_bottom_left.tile_code in Constants.TILES_WITH_COLLIDERS:
            if player_rect.colliderect(tile_rect_bottom_left):
                return False

        return True

    def to_rect(self, tile, cam_x, cam_y):

        x = tile.j * Constants.TILE_SIZE - cam_x
        y = tile.i * Constants.TILE_SIZE - cam_y

        return pygame.Rect(x, y, Constants.TILE_SIZE, Constants.TILE_SIZE)


    def unapply_camera(self, pos):
        x = pos[0] + self.camera.offset_x
        y = pos[1] + self.camera.offset_y
        return x, y


    def get_selected_tile_sprite(self, mouse_pos_raw):

        mouse_pos = self.unapply_camera(mouse_pos_raw)
        tile = self.screen_map.get_selected_tile(mouse_pos)

        x = tile.j * Constants.TILE_SIZE - self.camera.offset_x
        y = tile.i * Constants.TILE_SIZE - self.camera.offset_y

        return SelectedTile(x, y, tile.tile_code)


    def get_selected_tile(self, mouse_pos_raw):
        mouse_pos = self.unapply_camera(mouse_pos_raw)
        return self.screen_map.get_selected_tile(mouse_pos)


    def get_tile_under_player(self):
        player_pos = self.unapply_camera((Constants.GAME_SCREEN_CENTER_X_RAW, Constants.GAME_SCREEN_CENTER_Y_RAW))
        return self.screen_map.get_selected_tile(player_pos)


    def remove_selected_tile(self, mouse_pos_raw):
        mouse_pos = self.unapply_camera(mouse_pos_raw)
        self.screen_map.update_selected_tile(mouse_pos, Constants.TileCode.GRASS.value)

    def place_on_selected_tile(self, mouse_pos_raw, tile_code):
        mouse_pos = self.unapply_camera(mouse_pos_raw)
        self.screen_map.update_selected_tile(mouse_pos, tile_code)

    def remove_growing_tile(self, mouse_pos_raw):
        mouse_pos = self.unapply_camera(mouse_pos_raw)
        self.screen_map.remove_growing_tile(mouse_pos)

    def add_growing_tile(self, mouse_pos_raw, tile_code):
        mouse_pos = self.unapply_camera(mouse_pos_raw)
        self.screen_map.place_growing_tile(mouse_pos, tile_code)

    def get_move_list_to_tile(self, mouse_pos_raw):

        mouse_pos = self.unapply_camera(mouse_pos_raw)

        tile_list = self.screen_map.get_tile_list(mouse_pos, self.camera)

        if tile_list is None:
            return []


        move_list = self.get_move_to_center_moves()

        for i in range(len(tile_list) - 1):
            move_list += self.get_neighbour_moves(tile_list[i], tile_list[i + 1])

        return move_list

    def get_neighbour_moves(self, tile_1, tile_2):

        base_direction = (
            (tile_2[1] - tile_1[1]) * Constants.PLAYER_SPEED,
            (tile_2[0] - tile_1[0]) * Constants.PLAYER_SPEED
        )

        repeat = Constants.TILE_SIZE // Constants.PLAYER_SPEED

        moves = []

        while repeat:

            moves.append(base_direction)
            repeat -= 1

        return moves

    def get_move_to_center_moves(self):

        moves = []

        player_pos_raw = self.unapply_camera((Constants.GAME_SCREEN_CENTER_X, Constants.GAME_SCREEN_CENTER_Y))

        # player position inside the tile
        cam_x = player_pos_raw[0] % Constants.TILE_SIZE
        cam_y = player_pos_raw[1] % Constants.TILE_SIZE

        tile_center = Constants.TILE_SIZE // 2

        tile_min = tile_center - Constants.PLAYER_SPEED // 2
        tile_max = tile_center + Constants.PLAYER_SPEED // 2

        while tile_min > cam_x:
            cam_x += Constants.PLAYER_SPEED
            cam_x %= Constants.TILE_SIZE
            moves.append((Constants.PLAYER_SPEED, 0))

        while tile_max < cam_x:
            cam_x -= Constants.PLAYER_SPEED
            cam_x %= Constants.TILE_SIZE
            moves.append((-Constants.PLAYER_SPEED, 0))

        while tile_min > cam_y:
            cam_y += Constants.PLAYER_SPEED
            moves.append((0, Constants.PLAYER_SPEED))

        while tile_max < cam_y:
            cam_y -= Constants.PLAYER_SPEED
            moves.append((0, -Constants.PLAYER_SPEED))

        return moves


    def get_top_left_xy_from_ij(self, i, j):

        x = j * Constants.TILE_SIZE - self.camera.offset_x
        y = i * Constants.TILE_SIZE - self.camera.offset_y

        return x, y

class Camera:

    def __init__(self):
        self.offset_x = Singleton.player_stats.camera_offset_x
        self.offset_y = Singleton.player_stats.camera_offset_y

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

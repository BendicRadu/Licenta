from maps.WorldMap.WorldMap import WorldMap
from sprites.Tile import Tile
from util import Constants
from util.Singleton import Singleton


class ScreenMap:

    def __init__(self, chunk_offset = (5, 5), chunk_pos = Singleton.player.get_local_pos()):

        self.world_map = WorldMap()

        self.player = Singleton.player

        self.current_chunk_offset = chunk_offset
        self.chunk_pos = chunk_pos

        self.matrix = ScreenMapMatrix()
        self.update_tiles()

    def get_tiles(self):
        return self.matrix

    # Get global i and j for the PLAYER
    def get_global_i_j(self, offset_i = 0, offset_j = 0):

        chunk_i = self.current_chunk_offset[0]
        chunk_j = self.current_chunk_offset[1]

        chunk_pos_i = self.chunk_pos[0] + offset_i
        chunk_pos_j = self.chunk_pos[1] + offset_j

        global_i = chunk_i * Constants.CHUNK_SIZE + chunk_pos_i
        global_j = chunk_j * Constants.CHUNK_SIZE + chunk_pos_j

        return global_i, global_j


    def get_updated_chunk_offset(self, x, y):
        return (y // Constants.TILE_SIZE // Constants.CHUNK_SIZE,
                x // Constants.TILE_SIZE // Constants.CHUNK_SIZE)

    def get_updated_chunk_pos(self, x, y):
        return (y // Constants.TILE_SIZE % Constants.CHUNK_SIZE,
                x // Constants.TILE_SIZE % Constants.CHUNK_SIZE)

    def update_tiles(self):

        row_size    = Constants.WIDTH_NO_OF_TILES
        column_size = Constants.HEIGHT_NO_OF_TILES

        base_i, base_j = self.get_global_i_j(-Constants.HEIGHT_NO_OF_TILES // 2, -Constants.WIDTH_NO_OF_TILES // 2)

        for i in range(column_size):
            for j in range(row_size):

                tile = self.world_map.get_tile(base_i + i, base_j + j)
                self.matrix.add_tile(i, j, tile)


    def get_selected_tile(self, mouse_pos):

        mouse_i = mouse_pos[1] // Constants.TILE_SIZE
        mouse_j = mouse_pos[0] // Constants.TILE_SIZE

        global_mouse_i = self.current_chunk_offset[0] * Constants.CHUNK_SIZE + self.chunk_pos[0] + mouse_i
        global_mouse_j = self.current_chunk_offset[1] * Constants.CHUNK_SIZE + self.chunk_pos[1] + mouse_j

        tile_code = self.world_map.get_tile(global_mouse_i, global_mouse_j)

        return Tile(mouse_i, mouse_j, tile_code)

    # Returns True if the player was moved
    #         False if the player was not moved
    def move_player(self, direction):

        self.player.move(direction)

        self.current_chunk_offset = self.get_updated_chunk_offset(
            self.player.global_x,
            self.player.global_y
        )

        self.chunk_pos = self.get_updated_chunk_pos(
            self.player.global_x,
            self.player.global_y
        )


        self.update_tiles()

    def get_matrix_tile(self, i, j):
        return self.matrix.get_tile(i, j)

    def get_tile_from_screen(self, base_x, base_y, cam_x, cam_y):

        center_i = (base_y + cam_y) // Constants.TILE_SIZE
        center_j = (base_x + cam_x) // Constants.TILE_SIZE

        return Tile(
            center_i,
            center_j,
            self.matrix.get_tile(center_i, center_j)
        )


class ScreenMapMatrix:

    def __init__(self):
        self.height = Constants.HEIGHT_NO_OF_TILES
        self.width  = Constants.WIDTH_NO_OF_TILES
        self.matrix = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)

            self.matrix.append(row)


    def add_tile(self, i, j, tile):
        self.matrix[i][j] = tile


    def get_tile(self, i, j):
        return self.matrix[i][j]

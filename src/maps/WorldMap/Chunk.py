import csv
import datetime
import random
import time

from maps.WorldMap.ChunkGeneration import PerlinNoiseGenerator
from util import GameVars
from util.GameVars import BASE_PATH
from util.Singleton import Singleton


class Chunk:

    WORLD_MAP_DIR_PATH = BASE_PATH + "resources\\WorldMap\\"
    CHUNK_SUFFIX = "-chunk.txt"

    def __init__(self, offset_i, offset_j):

        self.offset_i = offset_i
        self.offset_j = offset_j

        self.chunk_mask = ChunkMask()
        self.tile_growth_service = Singleton.tile_growth_service
        self.generator = PerlinNoiseGenerator()

        self.matrix = []

        if self.is_chunk_generated():
            self.load_chunk()
        else:
            self.generate_chunk()


    def is_chunk_generated(self):

        # TODO Change to constant path

        file_path = self.WORLD_MAP_DIR_PATH \
                    + str(self.offset_i) + "-" + str(self.offset_j) + self.CHUNK_SUFFIX

        try:
            with open(file_path):
                return True

        except OSError:
            return False

    def load_chunk(self):

        file_path = self.WORLD_MAP_DIR_PATH \
                    + str(self.offset_i) + "-" + str(self.offset_j) + self.CHUNK_SUFFIX

        with open(file_path, "r") as file:
            for line in file:
                self.matrix.append(line.strip("\n").split(","))

    def _init_matrix(self):

        self.matrix = []

        for i in range(GameVars.CHUNK_SIZE):
            row = []
            for j in range(GameVars.CHUNK_SIZE):
                row.append(None)

            self.matrix.append(row)

    def generate_chunk(self):

        self._init_matrix()

        generation_matrix = self.generator.generate_chunk_matrix()

        growing_tile_batch = []

        for i in range(GameVars.CHUNK_SIZE):

            for j in range(GameVars.CHUNK_SIZE):

                generation_value = int(generation_matrix[i][j] * 1000)

                if GameVars.can_spawn_crafting_chest():
                    tile_code = GameVars.TileCode.CRAFTING_CHEST.value

                else:
                    tile_code = GameVars.get_tile_code_from_generation_value(generation_value)

                    if tile_code in GameVars.TILES_THAT_GROW:
                        global_pos = self.get_global_ij((i, j))
                        growing_tile_batch.append((global_pos[0], global_pos[1], tile_code,
                                                   int(round(time.time() * 1000) - 10000000)))


                self.matrix[i][j] = str(tile_code)


        self.chunk_mask.apply(self.matrix)

        if self.offset_i == 50 and self.offset_j == 50:
            self.apply_player_mask()

        self.add_growing_tiles(growing_tile_batch)
        self.save_chunk()

    def add_growing_tiles(self, growing_tile_batch):
        self.tile_growth_service.batch_insert(growing_tile_batch)

    def save_chunk(self):

        file_path = self.WORLD_MAP_DIR_PATH \
                + str(self.offset_i) + "-" + str(self.offset_j) + self.CHUNK_SUFFIX

        file = open(file_path, "w", newline='')

        for row in self.matrix:
            wr = csv.writer(file)
            wr.writerow(row)


    def update_tile(self, pos_tuple, tile_code):
        self.matrix[pos_tuple[0]][pos_tuple[1]] = tile_code
        self.save_chunk()

    def get_tile(self, pos_tuple):
        return self.matrix[pos_tuple[0]][pos_tuple[1]]

    def get_global_ij(self, pos):
        return (
            self.offset_i * GameVars.CHUNK_SIZE + pos[0],
            self.offset_j * GameVars.CHUNK_SIZE + pos[1]
        )

    def apply_player_mask(self):

        player = Singleton.player

        player_i, player_j = player.get_local_pos()

        for i in range(player_i - 2, player_i + 3):
            for j in range(player_j - 2, player_j + 3):
                self.matrix[i][j] = str(GameVars.TileCode.GRASS.value)

class ChunkMask:

    def __init__(self):

        self.mask = []
        self.init_mask()

    def init_mask(self):

        for i in range(GameVars.CHUNK_SIZE):
            row = []

            for j in range(GameVars.CHUNK_SIZE):
                row.append(not self.is_tile_in_circle(i, j))

            self.mask.append(row)


    # r - radius
    # n - resolution
    def is_tile_in_circle(self, i, j):

        x = ((j - GameVars.CHUNK_SIZE // 2) * GameVars.TILE_SIZE) + GameVars.TILE_SIZE / 2
        y = ((GameVars.CHUNK_SIZE - (i + GameVars.CHUNK_SIZE // 2)) * GameVars.TILE_SIZE) + GameVars.TILE_SIZE / 2

        radius = (GameVars.CHUNK_SIZE - 15) * GameVars.TILE_SIZE

        return abs(x) + abs(y) < radius


    def apply(self, map_matrix):

        for i in range(GameVars.CHUNK_SIZE):
            for j in range(GameVars.CHUNK_SIZE):

                if self.mask[i][j]:
                    map_matrix[i][j] = str(GameVars.spawn_tile())


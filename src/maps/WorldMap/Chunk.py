import csv
import datetime
import random
import time
from threading import Thread

from domain.GrowingTile import GrowingTile
from maps.WorldMap.PerlinNoise import banded_perlin_noise
from util import Constants
from util.Constants import TileCode
from util.Singleton import Singleton


class Chunk:

    def __init__(self, offset_i, offset_j):

        self.offset_i = offset_i
        self.offset_j = offset_j

        self.chunk_mask = ChunkMask()
        self.tile_growth_service = Singleton.tile_growth_service

        self.matrix = []

        if self.is_chunk_generated():
            self.load_chunk()
        else:
            self.generate_chunk()

    def is_chunk_generated(self):

        # TODO Change to constant path

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\" \
                    + str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

        try:
            with open(file_path):
                return True

        except OSError:
            return False

    def load_chunk(self):

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\" \
                    + str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

        with open(file_path, "r") as file:
            for line in file:
                self.matrix.append(line.strip("\n").split(","))

    def _init_matrix(self):

        self.matrix = []

        for i in range(Constants.CHUNK_SIZE):
            row = []
            for j in range(Constants.CHUNK_SIZE):
                row.append(None)

            self.matrix.append(row)

    def generate_chunk(self):

        self._init_matrix()

        perlin_matrix = banded_perlin_noise(Constants.CHUNK_SIZE,
                                            Constants.CHUNK_SIZE,
                                            [2, 4, 8, 16, 32, 64], [32, 16, 8, 4, 2, 1])

        growing_tile_batch = []

        for i in range(Constants.CHUNK_SIZE):

            for j in range(Constants.CHUNK_SIZE):

                perlin_value = int(perlin_matrix[i][j] * 1000)

                if Constants.can_spawn_crafting_chest():
                    tile_code = Constants.TileCode.CRAFTING_CHEST.value

                else:
                    tile_code = Constants.get_tile_code_from_perlin(perlin_value)

                    if tile_code in Constants.TILES_THAT_GROW:
                        global_pos = self.get_global_ij((i, j))
                        growing_tile_batch.append((global_pos[0], global_pos[1], tile_code, int(round(time.time() * 1000))))


                self.matrix[i][j] = str(tile_code)


        self.chunk_mask.apply(self.matrix)

        self.add_growing_tiles(growing_tile_batch)
        self.save_chunk()

    def add_growing_tiles(self, growing_tile_batch):
        self.tile_growth_service.batch_insert(growing_tile_batch)

    def save_chunk(self):

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\"
        file_path += str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

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
            self.offset_i * Constants.CHUNK_SIZE + pos[0],
            self.offset_j * Constants.CHUNK_SIZE + pos[1]
        )


class ChunkMask:

    def __init__(self):

        self.mask = []
        self.init_mask()

    def init_mask(self):

        for i in range(Constants.CHUNK_SIZE):
            row = []

            for j in range(Constants.CHUNK_SIZE):

                if self.is_tile_in_circle(i, j) or self.modifier():
                    row.append(False)
                else:
                    row.append(True)

            self.mask.append(row)




    # r - radius
    # n - resolution
    def is_tile_in_circle(self, i, j):

        x = ((j - Constants.CHUNK_SIZE // 2) * Constants.TILE_SIZE) + Constants.TILE_SIZE / 2
        y = ((Constants.CHUNK_SIZE - (i + Constants.CHUNK_SIZE // 2)) * Constants.TILE_SIZE) + Constants.TILE_SIZE / 2

        radius = (Constants.CHUNK_SIZE - 10) * Constants.TILE_SIZE

        return abs(x) + abs(y) < radius


    def apply(self, map_matrix):


        for i in range(Constants.CHUNK_SIZE):
            for j in range(Constants.CHUNK_SIZE):

                if self.mask[i][j]:
                    map_matrix[i][j] = str(Constants.spawn_tile())


    def modifier(self):
        return random.randint(0, 4) == 0

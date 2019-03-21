import datetime

from maps.WorldMap.Chunk import Chunk
from util import Constants

class WorldMap:


    def __init__(self):

        # Chunk map - The key is (offset_i, offset_j) and the value is the chunk
        self.chunk_map = {}


    def get_chunk_offset(self, i, j):
        return i // Constants.CHUNK_SIZE, j // Constants.CHUNK_SIZE

    def get_chunk_pos(self, i, j):
        return i % Constants.CHUNK_SIZE, j % Constants.CHUNK_SIZE

    def get_tile(self, i, j):

        chunk_offset = self.get_chunk_offset(i, j)
        chunk_pos    = self.get_chunk_pos(i, j)

        if chunk_offset not in self.chunk_map.keys():
            self.chunk_map[chunk_offset] = Chunk(chunk_offset[0], chunk_offset[1])

        return self.chunk_map[chunk_offset].get_tile(chunk_pos)

    def get_tile_by_offset(self, chunk_offset, chunk_pos):

        if chunk_offset not in self.chunk_map.keys():
            self.chunk_map[chunk_offset] = Chunk(chunk_offset[0], chunk_offset[1])

        return self.chunk_map[chunk_offset].get_tile(chunk_pos)

    def update_tile(self, i, j, tile_code):

        chunk_offset = self.get_chunk_offset(i, j)
        chunk_pos = self.get_chunk_pos(i, j)

        self.chunk_map[chunk_offset].update_tile(chunk_pos, tile_code)


def clear_unused_chunks(self):
        # TODO
        pass

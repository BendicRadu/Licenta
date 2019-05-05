from util import Constants


class TileGrowthCache:

    def __init__(self):
        self.cache = {}

    def contains(self, global_pos):

        to_be_removed = []

        for g_pos in self.cache.keys():

            i = global_pos[0]
            j = global_pos[1]

            i_cached = g_pos[0]
            j_cached = g_pos[1]

            if abs(i - i_cached) > Constants.CHUNK_SIZE or abs(j - j_cached) > Constants.CHUNK_SIZE:
                to_be_removed.append(g_pos)

        for g_pos in to_be_removed:
            del self.cache[g_pos]

        return global_pos in self.cache


    def get(self, global_pos):
        return self.cache[global_pos]

    def add(self, growing_tile):
        self.cache[growing_tile.global_pos] = growing_tile

    def remove(self, global_pos):
        del self.cache[global_pos]


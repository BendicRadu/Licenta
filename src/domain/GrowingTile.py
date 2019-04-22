import datetime

from util import Constants


class GrowingTile:

    def __init__(self, global_pos, tile_code, created_timestamp):
        self.global_pos = global_pos # (global_i, global_j)
        self.tile_code = tile_code
        self.created_timestamp = created_timestamp

class TileGrowthRate:

    # no_of stages: the number of growth stages
    # time_between_stages: measured in minutes
    def __init__(self, no_of_stages, time_between_stages):
        self.no_of_stages = no_of_stages
        self.time_between_stages = time_between_stages

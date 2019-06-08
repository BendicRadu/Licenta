import datetime

from mechanics.TileGrowthCache import TileGrowthCache
from mechanics.TileGrowthDao import TileGrowthDao
from util import GameVars


class TileGrowthService:

    def __init__(self):
        self.tile_growth_dao = TileGrowthDao()
        self.tile_growth_cache = TileGrowthCache()

    def add_growing_tile(self, global_pos, tile_code):
        self.tile_growth_dao.insert_growing_tile(global_pos, tile_code)

    def remove_growing_tile(self, global_pos):
        self.tile_growth_dao.delete_growing_tile(global_pos)
        self.tile_growth_cache.remove(global_pos)

    # tile_code is used if the growing tile is not in the db
    def get_tile_code_for_growth_tile(self, global_pos):

        if self.tile_growth_cache.contains(global_pos):
            growth_tile = self.tile_growth_cache.get(global_pos)
        else:
            growth_tile  = self.tile_growth_dao.get_growing_tile(global_pos)
            self.tile_growth_cache.add(growth_tile)

        tile_code    = growth_tile.tile_code
        created_time = growth_tile.created_timestamp

        growth_rate = GameVars.TILES_GROWTH_STAGES[tile_code]

        no_of_stages          = growth_rate.no_of_stages
        time_between_stages   = growth_rate.time_between_stages

        current_time = datetime.datetime.now()

        time_diff = current_time - created_time

        minute_diff = time_diff.total_seconds() // 60

        current_stage = 0

        while minute_diff - time_between_stages >= 0 and current_stage < no_of_stages:
            minute_diff -= time_between_stages
            current_stage += 1

        if current_stage == 0:
            return tile_code
        else:
            return tile_code + "_" + str(current_stage)

    def batch_insert(self, growing_tiles_batch):
        self.tile_growth_dao.batch_insert(growing_tiles_batch)
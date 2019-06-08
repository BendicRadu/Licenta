from mechanics.PlayerStats import PlayerStats
from mechanics.TileGrowthService import TileGrowthService
from sprites.Player import Player
from ui.inventory.Inventory import Inventory

class Singleton:

    inventory            = Inventory()
    tile_growth_service  = TileGrowthService()
    player_stats         = PlayerStats()
    player               = Player(player_stats.global_player_x, player_stats.global_player_y)



from sprites.Player import Player
from ui.inventory.Inventory import Inventory
from util import Constants
from util.ImageLoader import ImageLoader


class Singleton:

    imageLoader = ImageLoader()
    inventory   = Inventory()
    player      = Player(500 * Constants.TILE_SIZE + Constants.MIDDLE_SCREEN_I,
                         500 * Constants.TILE_SIZE + Constants.MIDDLE_SCREEN_J)

from sprites.Player import Player
from util import Constants
from util.Camera import Camera
from util.ImageLoader import ImageLoader


class Singleton:

    imageLoader = ImageLoader()
    player      = Player(500 * Constants.TILE_SIZE + Constants.MIDDLE_SCREEN_I,
                         500 * Constants.TILE_SIZE + Constants.MIDDLE_SCREEN_J)

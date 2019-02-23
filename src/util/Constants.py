from enum import Enum

# -----------------------SIZES----------------------------------------

# WIDTH = HEIGHT = *_SIZE

CHUNK_SIZE = 100
PLAYER_SIZE = 20
TILE_SIZE = 50

# Playable area
GAME_SCREEN_WIDTH = 1200
GAME_SCREEN_HEIGHT = 800

# Whole game window (With UI)
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1200

# -----------------------GAME-STATS------------------------------------

PLAYER_SPEED = 10

PLAYER_SCREEN_X = int(GAME_SCREEN_WIDTH / 2 - PLAYER_SIZE / 2)
PLAYER_SCREEN_Y = int(GAME_SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2)

PLAYER_SCREEN_X_RAW = GAME_SCREEN_WIDTH / 2 - PLAYER_SIZE / 2
PLAYER_SCREEN_Y_RAW = GAME_SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2

# Number of tiles that fit on the game screen + a little buffer
WIDTH_NO_OF_TILES  = GAME_SCREEN_WIDTH // TILE_SIZE + 2
HEIGHT_NO_OF_TILES = GAME_SCREEN_HEIGHT // TILE_SIZE + 2

# -----------------------MAP-GENERATION--------------------------------

# Trees, rocks, etc. to be placed on the map

# When generating the chunk, a random index is chosen
SPAWN_CHANCE_LIST = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2]

CHUNK_MIDDLE_OFFSET_I = 50
CHUNK_MIDDLE_OFFSET_J = 50

MIDDLE_SCREEN_I = HEIGHT_NO_OF_TILES // 2 // TILE_SIZE
MIDDLE_SCREEN_J = WIDTH_NO_OF_TILES // 2 // TILE_SIZE

class TileCode(Enum):
    GRASS = 0,
    ROCK = 1,
    TREE = 2


TILES_WITH_COLLIDERS = [1, 2]


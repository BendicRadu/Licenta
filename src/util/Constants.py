from enum import Enum

# -----------------------SIZES----------------------------------------

# WIDTH = HEIGHT = *_SIZE
from numpy.random.mtrand import randint
from pygame.rect import Rect

from ui.crafting.CraftingItem import CraftingItem

PERLIN_BUFFER = 2

CHUNK_SIZE = 100
PLAYER_SIZE = 23
TILE_SIZE = 55


# Playable area
GAME_SCREEN_WIDTH = 1400
GAME_SCREEN_HEIGHT = 1080

GAME_SCREEN_WIDTH_COPY = 1400
GAME_SCREEN_HEIGHT_COPY = 1080

GAME_SCREEN_RECT = Rect(0, 0, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

GAME_SCREEN_CENTER_X = GAME_SCREEN_WIDTH // 2
GAME_SCREEN_CENTER_Y = GAME_SCREEN_HEIGHT // 2

# Whole game window (With ui)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080



# ui (crafting and inventory)
UI_WIDTH  = SCREEN_WIDTH - GAME_SCREEN_WIDTH
UI_HEIGHT = SCREEN_HEIGHT

# -----------------------GAME-STATS------------------------------------

HP_BOX_HEIGHT = 5

SIGHT_RADIUS = GAME_SCREEN_WIDTH + 100

PLAYER_SPEED = 4

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
SPAWN_CHANCE_LIST = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     2, 2]



CHUNK_MIDDLE_OFFSET_I = 50
CHUNK_MIDDLE_OFFSET_J = 50

MIDDLE_SCREEN_I = HEIGHT_NO_OF_TILES // 2 // TILE_SIZE
MIDDLE_SCREEN_J = WIDTH_NO_OF_TILES // 2 // TILE_SIZE


class TileCode(Enum):
    NaN   = '-1'
    GRASS = '0'
    ROCK  = '1'
    TREE  = '2'
    WATER = '4'
    WOOD_FLOOR = '5'

    CRAFTING_CHEST = '1000'

    @staticmethod
    def get_random_tile():
        return SPAWN_CHANCE_LIST[randint(0, len(SPAWN_CHANCE_LIST))]

    @staticmethod
    def get_description(value):

        value = int(value)

        if value == 0:
            return "Grass"
        elif value == 1:
            return "Some rocks"
        elif value == 2:
            return "A tree"
        elif value == 4:
            return "Water"

# How long does it take to break a tile
TILE_HIT_POINTS= {
    TileCode.ROCK.value: 100,
    TileCode.TREE.value: 50,
    TileCode.WOOD_FLOOR.value: 50,
    TileCode.CRAFTING_CHEST.value: 200
}



class Direction(Enum):
    DOWN  = 0
    UP    = 1
    LEFT  = 2
    RIGHT = 3


TILES_WITH_COLLIDERS = ['1', '2', '4', '1000']
TILES_BUILDABLE = ['0', '4']
TILES_BREAKABLE = ['1', '2', '5', '1000']
TILES_OPAQUE = ['1', '-1']

TILES_ORE = ['1']

# INVENTORY --------------------------------------

INVENTORY_CELL_SIZE = 80

# (x, y)
INVENTORY_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 580)
INVENTORY_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 1080)

INVENTORY_TOP_RIGHT = (GAME_SCREEN_WIDTH + 500, 580)
INVENTORY_BOT_RIGHT = (GAME_SCREEN_WIDTH + 500, 1080)

INVENTORY_SCREEN_WIDTH  = INVENTORY_TOP_RIGHT[0] - INVENTORY_TOP_LEFT[0]
INVENTORY_SCREEN_HEIGHT = INVENTORY_BOT_LEFT[1] - INVENTORY_TOP_LEFT[1]

INVENTORY_MATRIX_WIDTH  = INVENTORY_SCREEN_WIDTH  // INVENTORY_CELL_SIZE
INVENTORY_MATRIX_HEIGHT = INVENTORY_SCREEN_HEIGHT // INVENTORY_CELL_SIZE

INVENTORY_RECT = Rect(INVENTORY_TOP_LEFT[0], INVENTORY_TOP_LEFT[1], INVENTORY_SCREEN_WIDTH, INVENTORY_SCREEN_HEIGHT)

ITEM_STACK_SIZE = 5

INVENTORY_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 558)

# CRAFTING -----------------------------------------------------

CRAFTING_CELL_SIZE = 80

CRAFTING_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 30)
CRAFTING_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 430)

CRAFTING_TOP_RIGHT = (GAME_SCREEN_WIDTH + 500, 30)
CRAFTING_BOT_RIGHT = (GAME_SCREEN_WIDTH + 500, 430)

CRAFTING_SCREEN_WIDTH  = CRAFTING_TOP_RIGHT[0] - CRAFTING_TOP_LEFT[0]
CRAFTING_SCREEN_HEIGHT = CRAFTING_BOT_LEFT[1]  - CRAFTING_TOP_LEFT[1]

CRAFTING_MATRIX_WIDTH  = CRAFTING_SCREEN_WIDTH  // CRAFTING_CELL_SIZE
CRAFTING_MATRIX_HEIGHT = CRAFTING_SCREEN_HEIGHT // CRAFTING_CELL_SIZE


CRAFTING_RECT = Rect(CRAFTING_TOP_LEFT[0], CRAFTING_TOP_LEFT[1], CRAFTING_SCREEN_WIDTH, CRAFTING_SCREEN_HEIGHT)

CRAFTING_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 8)


# TOOLS --------------------------------------------------

REQUIRED_ITEMS_CELL_SIZE = 80

REQUIRED_ITEMS_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 465)
REQUIRED_ITEMS_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 545)

REQUIRED_ITEMS_TOP_RIGHT = (GAME_SCREEN_WIDTH + 500, 465)
REQUIRED_ITEMS_BOT_RIGHT = (GAME_SCREEN_WIDTH + 500, 545)

REQUIRED_ITEMS_SCREEN_WIDTH  = REQUIRED_ITEMS_TOP_RIGHT[0] - REQUIRED_ITEMS_TOP_LEFT[0]
REQUIRED_ITEMS_SCREEN_HEIGHT = REQUIRED_ITEMS_BOT_LEFT[1]  - REQUIRED_ITEMS_TOP_LEFT[1]

REQUIRED_ITEMS_WIDTH  = REQUIRED_ITEMS_SCREEN_WIDTH  // REQUIRED_ITEMS_SCREEN_HEIGHT - 1

REQUIRED_ITEMS_RECT = Rect(REQUIRED_ITEMS_TOP_LEFT[0], REQUIRED_ITEMS_TOP_LEFT[1],
                           REQUIRED_ITEMS_SCREEN_WIDTH, REQUIRED_ITEMS_SCREEN_HEIGHT)

REQUIRED_ITEMS_LIST_WIDTH = REQUIRED_ITEMS_WIDTH  // REQUIRED_ITEMS_CELL_SIZE

REQUIRED_ITEMS_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 442)

CRAFT_BUTTON_TOP_LEFT = (GAME_SCREEN_WIDTH + 20 + REQUIRED_ITEMS_WIDTH * REQUIRED_ITEMS_CELL_SIZE, 465)

CRAFT_BUTTON_RECT     = Rect(CRAFT_BUTTON_TOP_LEFT[0], CRAFT_BUTTON_TOP_LEFT[1],
                             REQUIRED_ITEMS_CELL_SIZE, REQUIRED_ITEMS_CELL_SIZE)

CRAFT_BUTTON_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20 + REQUIRED_ITEMS_WIDTH * REQUIRED_ITEMS_CELL_SIZE + 3, 442)

def get_tile_code_from_perlin(perlin_value):

    k = perlin_value

    if k < 260:

        object_type = TileCode.WATER.value

        if 100 < k < 110:
            object_type = TileCode.get_random_tile()

    elif 260 <= k < 270:
        object_type = TileCode.TREE.value


    elif 270 <= k < 520:
        object_type = TileCode.get_random_tile()

    elif 520 <= k < 700:
        object_type = TileCode.TREE.value

    else:
        object_type = TileCode.ROCK.value


    return object_type


def get_tile_code_for_buffer():
    i = randint(0, len(SPAWN_CHANCE_LIST))
    return str(SPAWN_CHANCE_LIST[i])




def spawn_tile():
    return SPAWN_CHANCE_LIST[randint(0, len(SPAWN_CHANCE_LIST))]


def can_spawn_crafting_chest():
    return randint(0, CHUNK_SIZE * CHUNK_SIZE) < 5

class CraftingItems(Enum):

    WOOD_FLOOR = CraftingItem(

        # TODO Change to appropriate tile code

        TileCode.TREE.value,
        {
            TileCode.TREE.value: 1
        }
    )

    ROCK_FLOOR = CraftingItem(

        # TODO here too

        TileCode.ROCK.value,
        {
            TileCode.ROCK.value: 1
        }
    )

    # TODO Remove this :)
    MAGIC_TILE = CraftingItem(

        TileCode.WOOD_FLOOR.value,
        {
            TileCode.TREE.value: 2,
            TileCode.ROCK.value: 2
        }
    )

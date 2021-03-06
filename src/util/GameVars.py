import os
from enum import Enum

# -----------------------SIZES----------------------------------------

# WIDTH = HEIGHT = *_SIZE
from numpy.random.mtrand import randint
from pygame.rect import Rect

from domain.GrowingTile import TileGrowthRate
from ui.crafting.CraftingItem import CraftingItem

_cwd = os.getcwd()

BASE_PATH = ""

for i in _cwd.split("\\"):
    if i == "LicentaApp":
        BASE_PATH += i + "\\"
        break

    BASE_PATH += i + "\\"


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

    @staticmethod
    def get_direction_vector(direction):

        if direction == Direction.DOWN:
            return 0, 1

        elif direction == Direction.UP:
            return 0, -1

        elif direction == Direction.LEFT:
            return -1, 0

        elif direction == Direction.RIGHT:
            return 1, 0

    @staticmethod
    def get_direction_from_vector(vector):

        if vector == (0, 1):
            return Direction.DOWN

        elif vector == (0, -1):
            return Direction.UP

        elif vector == (-1, 0):
            return Direction.LEFT

        elif vector == (1, 0):
            return Direction.RIGHT

    @staticmethod
    def are_opposing(d1, d2):

        if d1 == Direction.UP and d2 == Direction.DOWN:
            return True

        elif d1 == Direction.DOWN and d2 == Direction.UP:
            return True

        elif d1 == Direction.LEFT and d2 == Direction.RIGHT:
            return True

        elif d1 == Direction.RIGHT and d2 == Direction.LEFT:
            return True

        return False


PERLIN_BUFFER = 2

CHUNK_SIZE = 100
PLAYER_SIZE = 23
TILE_SIZE = 55

# Playable area
GAME_SCREEN_WIDTH = 1000
GAME_SCREEN_HEIGHT = 800

GAME_SCREEN_RECT = Rect(0, 0, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

GAME_SCREEN_CENTER_X = GAME_SCREEN_WIDTH // 2
GAME_SCREEN_CENTER_Y = GAME_SCREEN_HEIGHT // 2

GAME_SCREEN_CENTER_X_RAW = GAME_SCREEN_WIDTH // 2
GAME_SCREEN_CENTER_Y_RAW = GAME_SCREEN_HEIGHT // 2

# Whole game window (With ui)
SCREEN_WIDTH = 1390
SCREEN_HEIGHT = 800

# ui (crafting and inventory)
UI_WIDTH = SCREEN_WIDTH - GAME_SCREEN_WIDTH
UI_HEIGHT = SCREEN_HEIGHT

# -----------------------GAME-STATS------------------------------------

HP_BOX_HEIGHT = 5

SIGHT_RADIUS = GAME_SCREEN_WIDTH + 100

PLAYER_SPEED = 5

PLAYER_SCREEN_X = int(GAME_SCREEN_WIDTH / 2 - PLAYER_SIZE / 2)
PLAYER_SCREEN_Y = int(GAME_SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2)

PLAYER_SCREEN_X_RAW = GAME_SCREEN_WIDTH / 2 - PLAYER_SIZE / 2
PLAYER_SCREEN_Y_RAW = GAME_SCREEN_HEIGHT / 2 - PLAYER_SIZE / 2

# Number of tiles that fit on the game screen + a little buffer
WIDTH_NO_OF_TILES = GAME_SCREEN_WIDTH // TILE_SIZE + 2
HEIGHT_NO_OF_TILES = GAME_SCREEN_HEIGHT // TILE_SIZE + 2

# -----------------------MAP-GENERATION--------------------------------

# Trees, rocks, etc. to be placed on the map

# When generating the chunk, a random index is chosen
SPAWN_CHANCE_LIST = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     2, 2]

MIDDLE_SCREEN_I = HEIGHT_NO_OF_TILES // 2 // TILE_SIZE
MIDDLE_SCREEN_J = WIDTH_NO_OF_TILES // 2 // TILE_SIZE


class TileCode(Enum):
    NaN = '-1'
    GRASS = '0'
    ROCK = '1'
    ROCK_FRONT = '1_1'
    ROCK_TOP = '1_2'
    TREE = '2'
    WATER = '4'
    WOOD_FLOOR = '5'
    WHEAT_SEEDS = '6'
    WHEAT_GROWING = '6_1'
    WHEAT = '6_2'
    WHEAT_TOP = '6_3'
    BREAD = '7'

    MOVER_RIGHT = '8'
    MOVER_LEFT = '9'
    MOVER_UP = '10'
    MOVER_DOWN = '11'

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
TILE_HIT_POINTS = {
    TileCode.ROCK.value: 40,
    TileCode.ROCK_FRONT.value: 40,
    TileCode.ROCK_TOP.value: 40,

    TileCode.TREE.value: 20,
    TileCode.WOOD_FLOOR.value: 20,
    TileCode.CRAFTING_CHEST.value: 40,
    TileCode.WHEAT_SEEDS.value: 10,
    TileCode.WHEAT_GROWING.value: 10,
    TileCode.WHEAT.value: 10,
    TileCode.WHEAT_TOP.value: 10,

    TileCode.MOVER_RIGHT.value: 1,
    TileCode.MOVER_RIGHT.value + "_1": 1,
    TileCode.MOVER_RIGHT.value + "_2": 1,
    TileCode.MOVER_RIGHT.value + "_3": 1,
    TileCode.MOVER_RIGHT.value + "_4": 1,

    TileCode.MOVER_LEFT.value: 1,
    TileCode.MOVER_LEFT.value + "_1": 1,
    TileCode.MOVER_LEFT.value + "_2": 1,
    TileCode.MOVER_LEFT.value + "_3": 1,
    TileCode.MOVER_LEFT.value + "_4": 1,

    TileCode.MOVER_UP.value: 1,
    TileCode.MOVER_UP.value + "_1": 1,
    TileCode.MOVER_UP.value + "_2": 1,
    TileCode.MOVER_UP.value + "_3": 1,
    TileCode.MOVER_UP.value + "_4": 1,

    TileCode.MOVER_DOWN.value: 1,
    TileCode.MOVER_DOWN.value + "_1": 1,
    TileCode.MOVER_DOWN.value + "_2": 1,
    TileCode.MOVER_DOWN.value + "_3": 1,
    TileCode.MOVER_DOWN.value + "_4": 1,
}

TILES_WITH_COLLIDERS = [
    TileCode.ROCK.value,
    TileCode.ROCK_FRONT.value,
    TileCode.ROCK_TOP.value,
    TileCode.TREE.value,
    TileCode.WATER.value,
    TileCode.CRAFTING_CHEST.value,

    TileCode.WHEAT.value,
    TileCode.WHEAT_TOP.value
]

TILES_BUILDABLE = [
    TileCode.GRASS.value,
    TileCode.WATER.value
]

NaN = '-1'
GRASS = '0'
ROCK = '1'
TREE = '2'
WATER = '4'
WOOD_FLOOR = '5'
WHEAT_SEEDS = '6'
WHEAT_GROWING = '6_1'
WHEAT = '6_2'
BREAD = '7'

MOVER_RIGHT = '8'
MOVER_LEFT = '9'
MOVER_UP = '10'
MOVER_DOWN = '11'

CRAFTING_CHEST = '1000'


TILES_ANIMATED = [

    TileCode.MOVER_RIGHT.value,
    TileCode.MOVER_RIGHT.value + "_1",
    TileCode.MOVER_RIGHT.value + "_2",
    TileCode.MOVER_RIGHT.value + "_3",
    TileCode.MOVER_RIGHT.value + "_4",

    TileCode.MOVER_LEFT.value,
    TileCode.MOVER_LEFT.value + "_1",
    TileCode.MOVER_LEFT.value + "_2",
    TileCode.MOVER_LEFT.value + "_3",
    TileCode.MOVER_LEFT.value + "_4",

    TileCode.MOVER_UP.value,
    TileCode.MOVER_UP.value + "_1",
    TileCode.MOVER_UP.value + "_2",
    TileCode.MOVER_UP.value + "_3",
    TileCode.MOVER_UP.value + "_4",

    TileCode.MOVER_DOWN.value,
    TileCode.MOVER_DOWN.value + "_1",
    TileCode.MOVER_DOWN.value + "_2",
    TileCode.MOVER_DOWN.value + "_3",
    TileCode.MOVER_DOWN.value + "_4",
]


TILES_BREAKABLE = [
    TileCode.ROCK.value,
    TileCode.ROCK_FRONT.value,
    TileCode.ROCK_TOP.value,
    TileCode.TREE.value,
    TileCode.WOOD_FLOOR.value,
    TileCode.CRAFTING_CHEST.value,
    TileCode.WHEAT_SEEDS.value,
    TileCode.WHEAT_GROWING.value,
    TileCode.WHEAT.value,
    TileCode.WHEAT_TOP.value
]

TILES_BREAKABLE.extend(TILES_ANIMATED)

TILES_OPAQUE = [TileCode.ROCK.value, TileCode.NaN.value]
TILES_ORE = [TileCode.ROCK.value]
TILES_THAT_GROW = [TileCode.WHEAT_SEEDS.value,
                   TileCode.WHEAT_GROWING.value,
                   TileCode.WHEAT_TOP.value,
                   TileCode.WHEAT.value
                   ]

TILES_ANIMATION_FRAMES = {
    TileCode.MOVER_RIGHT.value: 5,
    TileCode.MOVER_LEFT.value: 5,
    TileCode.MOVER_UP.value: 5,
    TileCode.MOVER_DOWN.value: 5
}


# Tiles that move the players
TILES_MOVERS_DIRECTIONS = {

    TileCode.MOVER_RIGHT.value: Direction.RIGHT,
    TileCode.MOVER_RIGHT.value + "_1": Direction.RIGHT,
    TileCode.MOVER_RIGHT.value + "_2": Direction.RIGHT,
    TileCode.MOVER_RIGHT.value + "_3": Direction.RIGHT,
    TileCode.MOVER_RIGHT.value + "_4": Direction.RIGHT,

    TileCode.MOVER_LEFT.value: Direction.LEFT,
    TileCode.MOVER_LEFT.value + "_1": Direction.LEFT,
    TileCode.MOVER_LEFT.value + "_2": Direction.LEFT,
    TileCode.MOVER_LEFT.value + "_3": Direction.LEFT,
    TileCode.MOVER_LEFT.value + "_4": Direction.LEFT,

    TileCode.MOVER_UP.value: Direction.UP,
    TileCode.MOVER_UP.value + "_1": Direction.UP,
    TileCode.MOVER_UP.value + "_2": Direction.UP,
    TileCode.MOVER_UP.value + "_3": Direction.UP,
    TileCode.MOVER_UP.value + "_4": Direction.UP,

    TileCode.MOVER_DOWN.value: Direction.DOWN,
    TileCode.MOVER_DOWN.value + "_1": Direction.DOWN,
    TileCode.MOVER_DOWN.value + "_2": Direction.DOWN,
    TileCode.MOVER_DOWN.value + "_3": Direction.DOWN,
    TileCode.MOVER_DOWN.value + "_4": Direction.DOWN,

}

TILES_MOVERS_SPEEDS = {

    TileCode.MOVER_RIGHT.value: 10,
    TileCode.MOVER_RIGHT.value + "_1": 10,
    TileCode.MOVER_RIGHT.value + "_2": 10,
    TileCode.MOVER_RIGHT.value + "_3": 10,
    TileCode.MOVER_RIGHT.value + "_4": 10,

    TileCode.MOVER_LEFT.value: 10,
    TileCode.MOVER_LEFT.value + "_1": 10,
    TileCode.MOVER_LEFT.value + "_2": 10,
    TileCode.MOVER_LEFT.value + "_3": 10,
    TileCode.MOVER_LEFT.value + "_4": 10,

    TileCode.MOVER_UP.value: 10,
    TileCode.MOVER_UP.value + "_1": 10,
    TileCode.MOVER_UP.value + "_2": 10,
    TileCode.MOVER_UP.value + "_3": 10,
    TileCode.MOVER_UP.value + "_4": 10,

    TileCode.MOVER_DOWN.value: 10,
    TileCode.MOVER_DOWN.value + "_1": 10,
    TileCode.MOVER_DOWN.value + "_2": 10,
    TileCode.MOVER_DOWN.value + "_3": 10,
    TileCode.MOVER_DOWN.value + "_4": 10
}

# Time until player hunger decreases in minutes
HUNGER_TICK_DURATION = 1

# Value to substract from player hunger every hunger tick
HUNGER_TICK_VALUE = 10

FOOD_ITEMS = [
    TileCode.BREAD.value
]

FOOD_VALUES = {
    TileCode.BREAD.value: 10
}

ITEMS_PLACEABLE = [
    TileCode.ROCK.value,
    TileCode.TREE.value,
    TileCode.WOOD_FLOOR.value,
    TileCode.WHEAT_SEEDS.value,
    TileCode.MOVER_RIGHT.value,
    TileCode.MOVER_LEFT.value,
    TileCode.MOVER_UP.value,
    TileCode.MOVER_DOWN.value
]

# TileGrowthRate(no_of_stages, time_between_stages)
# time_between_stages is measured in minutes
TILES_GROWTH_STAGES = {
    TileCode.WHEAT_SEEDS.value: TileGrowthRate(2, 1)
}

# Maps a tile as a key and the items dropped when the tile breaks as a value

TILES_ITEM_MAP = {

    TileCode.ROCK.value: [TileCode.ROCK.value],
    TileCode.ROCK_FRONT.value: [TileCode.ROCK.value],
    TileCode.ROCK_TOP.value: [TileCode.ROCK.value],

    TileCode.TREE.value: [TileCode.TREE.value],
    TileCode.WOOD_FLOOR.value: [TileCode.WOOD_FLOOR.value],
    TileCode.WHEAT_SEEDS.value: [TileCode.WHEAT_SEEDS.value],
    TileCode.WHEAT_GROWING.value: [TileCode.WHEAT_SEEDS.value],
    TileCode.WHEAT.value: [TileCode.WHEAT_SEEDS.value, TileCode.WHEAT_SEEDS.value, TileCode.WHEAT.value],
    TileCode.WHEAT_TOP.value: [TileCode.WHEAT_SEEDS.value, TileCode.WHEAT_SEEDS.value, TileCode.WHEAT.value],

    TileCode.MOVER_RIGHT.value: [TileCode.MOVER_RIGHT.value],
    TileCode.MOVER_RIGHT.value + "_1": [TileCode.MOVER_RIGHT.value],
    TileCode.MOVER_RIGHT.value + "_2": [TileCode.MOVER_RIGHT.value],
    TileCode.MOVER_RIGHT.value + "_3": [TileCode.MOVER_RIGHT.value],
    TileCode.MOVER_RIGHT.value + "_4": [TileCode.MOVER_RIGHT.value],

    TileCode.MOVER_LEFT.value: [TileCode.MOVER_LEFT.value],
    TileCode.MOVER_LEFT.value + "_1": [TileCode.MOVER_LEFT.value],
    TileCode.MOVER_LEFT.value + "_2": [TileCode.MOVER_LEFT.value],
    TileCode.MOVER_LEFT.value + "_3": [TileCode.MOVER_LEFT.value],
    TileCode.MOVER_LEFT.value + "_4": [TileCode.MOVER_LEFT.value],

    TileCode.MOVER_UP.value: [TileCode.MOVER_UP.value],
    TileCode.MOVER_UP.value + "_1": [TileCode.MOVER_UP.value],
    TileCode.MOVER_UP.value + "_2": [TileCode.MOVER_UP.value],
    TileCode.MOVER_UP.value + "_3": [TileCode.MOVER_UP.value],
    TileCode.MOVER_UP.value + "_4": [TileCode.MOVER_UP.value],

    TileCode.MOVER_DOWN.value: [TileCode.MOVER_DOWN.value],
    TileCode.MOVER_DOWN.value + "_1": [TileCode.MOVER_DOWN.value],
    TileCode.MOVER_DOWN.value + "_2": [TileCode.MOVER_DOWN.value],
    TileCode.MOVER_DOWN.value + "_3": [TileCode.MOVER_DOWN.value],
    TileCode.MOVER_DOWN.value + "_4": [TileCode.MOVER_DOWN.value],

}

# INVENTORY --------------------------------------

INVENTORY_CELL_SIZE = 50

# (x, y)
INVENTORY_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 580 - 150)
INVENTORY_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 1060)

INVENTORY_TOP_RIGHT = (SCREEN_WIDTH - 20, 580 - 150)
INVENTORY_BOT_RIGHT = (SCREEN_WIDTH - 20, 1060)

INVENTORY_SCREEN_WIDTH = INVENTORY_TOP_RIGHT[0] - INVENTORY_TOP_LEFT[0]
INVENTORY_SCREEN_HEIGHT = INVENTORY_BOT_LEFT[1] - INVENTORY_TOP_LEFT[1]

INVENTORY_MATRIX_WIDTH = INVENTORY_SCREEN_WIDTH // INVENTORY_CELL_SIZE
INVENTORY_MATRIX_HEIGHT = INVENTORY_SCREEN_HEIGHT // INVENTORY_CELL_SIZE

INVENTORY_RECT = Rect(INVENTORY_TOP_LEFT[0], INVENTORY_TOP_LEFT[1], INVENTORY_SCREEN_WIDTH, INVENTORY_SCREEN_HEIGHT)

ITEM_STACK_SIZE = 5

INVENTORY_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 558 - 150)

# CRAFTING -----------------------------------------------------

CRAFTING_CELL_SIZE = 50

CRAFTING_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 30)
CRAFTING_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 430 - 150)

CRAFTING_TOP_RIGHT = (SCREEN_WIDTH - 20, 30)
CRAFTING_BOT_RIGHT = (SCREEN_WIDTH - 20, 430 - 150)

CRAFTING_SCREEN_WIDTH = CRAFTING_TOP_RIGHT[0] - CRAFTING_TOP_LEFT[0]
CRAFTING_SCREEN_HEIGHT = CRAFTING_BOT_LEFT[1] - CRAFTING_TOP_LEFT[1]

CRAFTING_MATRIX_WIDTH = CRAFTING_SCREEN_WIDTH // CRAFTING_CELL_SIZE
CRAFTING_MATRIX_HEIGHT = CRAFTING_SCREEN_HEIGHT // CRAFTING_CELL_SIZE

CRAFTING_RECT = Rect(CRAFTING_TOP_LEFT[0], CRAFTING_TOP_LEFT[1], CRAFTING_SCREEN_WIDTH, CRAFTING_SCREEN_HEIGHT)

CRAFTING_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 10, 4)

# TOOLS --------------------------------------------------

REQUIRED_ITEMS_CELL_SIZE = 50

REQUIRED_ITEMS_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 465 - 150)
REQUIRED_ITEMS_BOT_LEFT = (GAME_SCREEN_WIDTH + 20, 545 - 150)

REQUIRED_ITEMS_TOP_RIGHT = (SCREEN_WIDTH - 20, 465 - 150)
REQUIRED_ITEMS_BOT_RIGHT = (SCREEN_WIDTH - 20, 545 - 150)

REQUIRED_ITEMS_SCREEN_WIDTH = REQUIRED_ITEMS_TOP_RIGHT[0] - REQUIRED_ITEMS_TOP_LEFT[0]
REQUIRED_ITEMS_SCREEN_HEIGHT = REQUIRED_ITEMS_BOT_LEFT[1] - REQUIRED_ITEMS_TOP_LEFT[1]

REQUIRED_ITEMS_WIDTH = 6

REQUIRED_ITEMS_RECT = Rect(REQUIRED_ITEMS_TOP_LEFT[0], REQUIRED_ITEMS_TOP_LEFT[1],
                           REQUIRED_ITEMS_SCREEN_WIDTH, REQUIRED_ITEMS_SCREEN_HEIGHT)

REQUIRED_ITEMS_LIST_WIDTH = REQUIRED_ITEMS_WIDTH // REQUIRED_ITEMS_CELL_SIZE

REQUIRED_ITEMS_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20, 442 - 150)

CRAFT_BUTTON_TOP_LEFT = (GAME_SCREEN_WIDTH + 20 + REQUIRED_ITEMS_WIDTH * REQUIRED_ITEMS_CELL_SIZE, 465 - 150)

CRAFT_BUTTON_RECT = Rect(CRAFT_BUTTON_TOP_LEFT[0], CRAFT_BUTTON_TOP_LEFT[1],
                         REQUIRED_ITEMS_CELL_SIZE, REQUIRED_ITEMS_CELL_SIZE)

CRAFT_BUTTON_TEXT_TOP_LEFT = (GAME_SCREEN_WIDTH + 20 + REQUIRED_ITEMS_WIDTH * REQUIRED_ITEMS_CELL_SIZE + 3, 442 - 150)



HUNGER_BAR_X = GAME_SCREEN_WIDTH + 21
HUNGER_BAR_Y = UI_HEIGHT - 20

HUNGER_BAR_WIDTH = UI_WIDTH - 41
HUNGER_BAR_HEIGHT = 20

def get_random_mover():
    i = randint(0, 4)
    movers = ['8', '9', '10', '11']
    return movers[i]


def get_tile_code_from_generation_value(generation_value):
    k = generation_value

    # Water
    if k < 260:

        object_type = TileCode.WATER.value

        if 100 < k < 110:
            object_type = TileCode.get_random_tile()

    # Trees
    elif 260 <= k < 270:
        object_type = TileCode.TREE.value

    # Grass
    elif 270 <= k < 520:
        object_type = TileCode.get_random_tile()

        if 300 <= k < 320:
            object_type = TileCode.WHEAT_SEEDS.value

    # Trees
    elif 520 <= k < 700:
        object_type = TileCode.TREE.value

    # Rocks
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

    BREAD = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )

    MOVER_LEFT = CraftingItem(

        # TODO Change to appropriate tile code

        TileCode.MOVER_LEFT.value,
        {
            TileCode.ROCK.value: 1,
            TileCode.TREE.value: 1
        }
    )

    MOVER_RIGHT = CraftingItem(

        # TODO Change to appropriate tile code

        TileCode.MOVER_RIGHT.value,
        {
            TileCode.ROCK.value: 1
        }
    )

    MOVER_UP = CraftingItem(

        # TODO Change to appropriate tile code

        TileCode.MOVER_UP.value,
        {
            TileCode.ROCK.value: 1
        }
    )

    MOVER_DOWN = CraftingItem(

        # TODO Change to appropriate tile code

        TileCode.MOVER_DOWN.value,
        {
            TileCode.ROCK.value: 1
        }
    )

    BREAD2 = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )

    BREAD3 = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )

    BREAD4 = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )

    BREAD5 = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )

    BREAD6 = CraftingItem(

        # TODO here too

        TileCode.BREAD.value,
        {
            TileCode.WHEAT.value: 3
        }
    )


def normalize(vec):
    x, y = vec

    if x < 0:
        x = -1
    elif x > 0:
        x = 1

    if y < 0:
        y = -1
    elif y > 0:
        y = 1

    return x, y


def speed_vector_diff(player_vec, tile_vec):


    d1 = Direction.get_direction_from_vector(normalize(player_vec))
    d2 = Direction.get_direction_from_vector(normalize(tile_vec))

    if d1 == d2:
        return player_vec[0] // 2 + tile_vec[0], player_vec[1] // 2 + tile_vec[1]

    x, y = 0, 0

    return player_vec[0] // 2 + player_vec[0] // 4, player_vec[1] // 2 + player_vec[1] // 4

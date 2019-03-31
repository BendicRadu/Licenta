from util import Constants
from util.Constants import Direction


class Player:


    def __init__(self, global_x, global_y):

        self.global_x = global_x
        self.global_y = global_y

        self.direction = Direction.DOWN

    def reset_direction(self):
        self.direction = Direction.DOWN

    # :param: direction - tuple (dx, dy)
    def move(self, direction):

        x, y = direction

        if x > 0:
            self.direction = Direction.RIGHT
        elif x < 0:
            self.direction = Direction.LEFT

        if y > 0:
            self.direction = Direction.DOWN
        elif y < 0:
            self.direction = Direction.UP

        self.global_x += x
        self.global_y += y





    def mock_move(self, direction):
        return self.global_x + direction[0],\
               self.global_y + direction[1]

    def get_chunk_offset(self):
        return self.global_x // Constants.TILE_SIZE // Constants.CHUNK_SIZE, \
               self.global_x // Constants.TILE_SIZE // Constants.CHUNK_SIZE

    def get_local_pos(self):
        return self.global_y // Constants.TILE_SIZE % Constants.CHUNK_SIZE, \
               self.global_x // Constants.TILE_SIZE % Constants.CHUNK_SIZE



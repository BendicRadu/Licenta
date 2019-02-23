from util import Constants


class Player:


    def __init__(self, global_x, global_y):

        self.global_x = global_x
        self.global_y = global_y


    # :param: direction - tuple (dx, dy)
    def move(self, direction):

        self.global_x += direction[0]
        self.global_y += direction[1]

    def mock_move(self, direction):
        return self.global_x + direction[0],\
               self.global_y + direction[1]

    def get_local_pos(self):
        return self.global_y // Constants.TILE_SIZE % Constants.CHUNK_SIZE, \
               self.global_x // Constants.TILE_SIZE % Constants.CHUNK_SIZE


class Tile:

    def __init__(self, i, j, tile_code):

        self.i = i
        self.j = j
        self.tile_code = tile_code

    def __eq__(self, other):

        if other is None:
            return False

        return self.i == other.i and self.j == other.j and self.tile_code == other.tile_code

class SelectedTile:

    def __init__(self, x, y, tile_code):

        self.x = x
        self.y = y
        self.tile_code = tile_code

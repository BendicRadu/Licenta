from sprites.MapSprite import Sprite
from ui.crafting.Crafting import Crafting
from util import Constants


class RenderCrafting:

    def __init__(self):
        self.crafting = Crafting()


    def get_sprites(self):

        matrix = self.crafting.get_matrix()

        sprite_list = []

        for i in range(matrix.height):
            for j in range(matrix.width):
                tile_code = matrix[(i, j)]

                x = j * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[0]
                y = i * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[1]

                sprite = Sprite(x, y, tile_code)

                sprite_list.append(sprite)

        return sprite_list

from util import Constants
from util.Singleton import Singleton


class Crafting:

    def __init__(self):

        self.inventory = Singleton.inventory
        self.crafting_matrix = CraftingMatrix()

    def get_matrix(self):
        return self.crafting_matrix

    def craft(self, pos):

        if not self.__can_craft(pos):
            return

        self.__remove_items_for_crafting(pos)

        tile_code = self.crafting_matrix[pos].tile_code

        self.inventory.auto_add(tile_code, 1)


    def __remove_items_for_crafting(self, pos):

        item_to_craft = self.crafting_matrix[pos]
        required_items = item_to_craft.crafting_items_required

        for tile_code in required_items.keys():

            required_quantity = required_items[tile_code]

            self.inventory.remove(tile_code, required_quantity)

    def __can_craft(self, pos):

        item_to_craft = self.crafting_matrix[pos]
        required_items = item_to_craft.crafting_items_required

        for tile_code in required_items.keys():

            # required_items - map
            # - key   = tile_code
            # - value = quantity
            required_quantity = required_items[tile_code]

            if not self.inventory.is_in_inventory(tile_code, required_quantity):
                return False

        return True





class CraftingMatrix:

    def __init__(self):
        # TODO - change to hardcoded crafting matrix

        self.matrix = []

        self.width = Constants.CRAFTING_MATRIX_WIDTH
        self.height = Constants.CRAFTING_MATRIX_HEIGHT

        for i in range(self.height):

            matrix_row = []

            for j in range(self.width):
                matrix_row.append("0")

            self.matrix.append(matrix_row)



    def __getitem__(self, pos):
        return self.matrix[pos[0]][pos[1]]

    def __setitem__(self, pos, item):

        if item is None:
            self.matrix[pos[0]][pos[1]] = None

        else:
            item.is_virtual = False
            self.matrix[pos[0]][pos[1]] = item




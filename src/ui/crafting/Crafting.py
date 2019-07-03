from ui.crafting.CraftingItem import CraftingItem
from util import GameVars
from util.Singleton import Singleton


class Crafting:

    def __init__(self):

        self.inventory = Singleton.inventory
        self.crafting_matrix = CraftingMatrix(Singleton.player_stats.crafting_items_no)

        self.inventory_update_events = []
        self.selected_pos = None

    def get_crafting_items_no(self):
        return self.get_matrix().unlocked_items_no

    def is_selected_locked(self, pos):
        return self.get_matrix()[pos].is_empty_cell() or self.get_matrix()[pos].is_locked()

    def select(self, pos):
        if self.get_matrix()[pos].is_empty_cell() or self.get_matrix()[pos].is_locked():
            self.selected_pos = None

        self.selected_pos = pos

    def get_selected_pos(self):
        return self.selected_pos

    def get_selected(self):

        if self.selected_pos is None:
            return None

        return self.get_matrix()[self.selected_pos]

    def get_matrix(self):
        return self.crafting_matrix

    def craft(self):

        if not self.can_craft():
            return

        self.__remove_items_for_crafting(self.selected_pos)

        tile_code = self.crafting_matrix[self.selected_pos].tile_code

        return self.inventory.auto_add(tile_code, 1)


    def __remove_items_for_crafting(self, pos):

        item_to_craft = self.crafting_matrix[pos]
        required_items = item_to_craft.crafting_items_required

        for tile_code in required_items.keys():

            required_quantity = required_items[tile_code]

            self.inventory.remove(tile_code, required_quantity)

    def can_craft(self):

        if self.selected_pos is None:
            return False

        item_to_craft = self.crafting_matrix[self.selected_pos]

        if not item_to_craft.unlocked:
            return False

        required_items = item_to_craft.crafting_items_required

        for tile_code in required_items.keys():

            # required_items - map
            # - key   = tile_code
            # - value = quantity
            required_quantity = required_items[tile_code]

            if not self.inventory.is_in_inventory(tile_code, required_quantity):
                return False

        return True

    def unlock_next_item(self):
        return self.crafting_matrix.unlock_next_item()



class CraftingMatrix:

    def __init__(self, unlocked_items_no):
        # TODO - change to hardcoded crafting matrix

        self.matrix = []

        self.width = GameVars.CRAFTING_MATRIX_WIDTH
        self.height = GameVars.CRAFTING_MATRIX_HEIGHT

        self.unlocked_items_no = unlocked_items_no

        crafting_item_list = [crafting_item.value for crafting_item in GameVars.CraftingItems]
        current_item_index = 0

        for i in range(self.height):

            matrix_row = []

            for j in range(self.width):

                if current_item_index < len(crafting_item_list):

                    matrix_row.append(crafting_item_list[current_item_index])

                    if current_item_index < self.unlocked_items_no:
                        matrix_row[-1].unlocked = True

                    current_item_index += 1

                else:
                    matrix_row.append(CraftingItem.get_empty_cell())

            self.matrix.append(matrix_row)

    def unlock_next_item(self):
        self.unlocked_items_no += 1

        for i in range(self.height):
            for j in range(self.width):
                if not self[i, j].unlocked:
                    self[i, j].unlocked = True
                    return i, j

    def __getitem__(self, pos):
        return self.matrix[pos[0]][pos[1]]

    def __setitem__(self, pos, item):

        if item is None:
            self.matrix[pos[0]][pos[1]] = None

        else:
            item.is_virtual = False
            self.matrix[pos[0]][pos[1]] = item




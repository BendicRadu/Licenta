from ui.inventory.ItemStack import Item
from util import Constants


# select
# take_one
# auto_add
# split_begin
# split_end
# split_cancel
# noinspection PyUnresolvedReferences
class Inventory:

    def __init__(self):
        self.inventory_matrix = InventoryMatrix()

        self.__split_start_pos = None
        self.__split_virtual_item = None


    def is_item_selected(self):
        return self.inventory_matrix.selected_pos is not None

    def select(self, pos):

        if self.inventory_matrix[pos].is_empty_cell():
            return None

        self.inventory_matrix.selected_pos = pos
        return pos

    def get_item(self, pos):
        return self.inventory_matrix[pos]

    def take_one(self):
        return self.inventory_matrix.take_one(self.selected_pos)

    def auto_add(self, tile_code, quantity):

        add_pos = self.inventory_matrix.get_first_pos_of_type(tile_code)

        if add_pos is None:
            add_pos = self.inventory_matrix.get_first_free_pos()

        if add_pos is None:
            return False

        virtual_item = Item(tile_code, quantity, True)

        return self.inventory_matrix.add_item(virtual_item, add_pos)

    def split_begin(self, start_pos):

        self.__split_start_pos = start_pos
        self.__split_virtual_item = self.inventory_matrix.split_start(start_pos)

    def split_end(self, end_pos):

        added_pos = self.inventory_matrix.add_item(self.__split_virtual_item, end_pos)

        if added_pos is not None:
            self.inventory_matrix.split_finish(self.__split_start_pos)
        else:
            self.inventory_matrix.split_cancel(self.__split_start_pos)

        self.__reset_split()

    def split_cancel(self):
        self.inventory_matrix.split_cancel(self.__split_start_pos)
        self.__reset_split()

    def get_matrix(self):
        return self.inventory_matrix

    def __reset_split(self):
        self.__split_start_pos = None
        self.__split_virtual_item = None

    def __add(self, item, pos):
        return self.inventory_matrix.add_item(item, pos)

    def is_in_inventory(self, tile_code, quantity):

        amount_in_inventory = 0

        for i in range(self.inventory_matrix.height):
            for j in range(self.inventory_matrix.width):
                if self.inventory_matrix \
                        .get_item((i, j)) \
                        .tile_code == tile_code:

                    amount_in_inventory += self.inventory_matrix.get_item((i, j)).quantity

                    if amount_in_inventory >= quantity:
                        return True

        return False

    def remove(self, tile_code, quantity_to_be_removed):

        for i in range(self.inventory_matrix.height):
            for j in range(self.inventory_matrix.width):
                if self.inventory_matrix \
                        .get_item((i, j)) \
                        .tile_code == tile_code:

                    quantity_to_be_removed = self.inventory_matrix\
                        .remove(quantity_to_be_removed, (i, j))

                    if quantity_to_be_removed == 0:
                        return


    def select_item(self, pos):
        self.inventory_matrix.selected_pos = pos

    def get_selected_item(self):
        return self.inventory_matrix.get_selected_item()

    def remove_selected_item(self):
        self.inventory_matrix.remove_selected_item()

# Supports pos tuple indexing (pos[0] - i, pos[1] - j)
class InventoryMatrix:

    def __init__(self):

        # TODO store in file

        self.matrix = []
        self.width = Constants.INVENTORY_MATRIX_WIDTH
        self.height = Constants.INVENTORY_MATRIX_HEIGHT

        self.selected_pos = None

        for i in range(self.height):
            row = []
            for j in range(self.width):

                item = Item.get_empty_cell()
                row.append(item)

            self.matrix.append(row)

    def take_one(self, pos):
        return self[pos].take_one()

    def add_item(self, item, pos):

        if self[pos].is_empty_cell():
            self[pos] = item
            return pos

        elif self[pos].tile_code == item.tile_code:
            self[pos].combine(item)
            return pos

        return None

    def remove(self, quantity, pos):
        return self[pos].remove(quantity)

    def split_start(self, pos):
        return self[pos].split_start()

    def split_cancel(self, pos):
        self[pos].split_cancel()

    def split_finish(self, pos):
        self[pos].split_finish()

        if self[pos].is_empty():
            self[pos] = None

    def get_item(self, pos):

        if pos is None:
            return None

        return self[pos]

    def get_first_free_pos(self):
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j].is_empty_cell():
                    return i, j

        return None

    def get_first_pos_of_type(self, tile_code):
        for i in range(self.height):
            for j in range(self.width):
                if not self[i, j].is_empty_cell() and self[i, j].tile_code == tile_code and not self[i, j].is_full():
                    return i, j

        return None

    def get_selected_item(self):
        return self[self.selected_pos]

    def remove_selected_item(self):
        self[self.selected_pos] = Item.get_empty_cell()

    def __getitem__(self, pos):
        return self.matrix[pos[0]][pos[1]]

    def __setitem__(self, pos, item):

        if item.is_empty_cell():
            self.matrix[pos[0]][pos[1]] = Item.get_empty_cell()

        else:
            item.is_virtual = False
            self.matrix[pos[0]][pos[1]] = item

from util import Constants


class Item:

    def __init__(self, tile_code, quantity, is_virtual = False):

        self.tile_code = tile_code
        self.quantity  = quantity

        self.quantity_buffer = 0

        # not virtual - item in inventory
        # virtual     - item being dragged

        # dragged on the screen
        self.is_virtual = is_virtual

    @staticmethod
    def get_empty_cell():
        # TODO Change to empty inventory cell sprite
        return Item('-1', -1)

    def is_empty_cell(self):
        return self.tile_code == '-1' and self.quantity == -1

    def split_start(self):

        if self.quantity == 1:
            return None

        self.quantity_buffer = self.quantity // 2
        self.quantity -= self.quantity // 2

        return Item(self.tile_code, self.quantity, True)

    def split_finish(self):
        self.quantity_buffer = 0

    def split_cancel(self):
        self.quantity += self.quantity_buffer
        self.quantity_buffer = 0


    def combine(self, other):

        if not other.is_virtual:
            raise Exception("Can only combine non virtual with virtual items")

        self.quantity += other.quantity

    def take_one(self):
        self.quantity -= 1
        return self.tile_code

    # tries to remove :quantity: items. If it can't, it returns the remaining items that need to be removed
    def remove(self, quantity):

        if self.quantity < quantity:
            self.quantity = 0
            return quantity - self.quantity

        self.quantity -= quantity
        return 0

    def add_one(self):
        self.quantity += 1

    def is_empty(self):
        return self.quantity == 0

    def is_full(self):
        return self.quantity == Constants.ITEM_STACK_SIZE

    def __repr__(self):
        return "Item ( tile_code = " + str(self.tile_code) + ", quantity = " + str(self.quantity) + ", virtual = " + str(self.is_virtual) + " )"

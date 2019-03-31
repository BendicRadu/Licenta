class CraftingItem:

    # crafting_items_required map
    # with key = tile_code
    # value = quantity
    def __init__(self, tile_code, crafting_items_required, unlocked = False):
        self.tile_code = tile_code
        self.crafting_items_required = crafting_items_required
        self.unlocked = unlocked


    @staticmethod
    def get_empty_cell():
        item = CraftingItem("-1", None)
        return item

    def is_empty_cell(self):
        return self.tile_code == "-1" and self.crafting_items_required is None

    def is_locked(self):
        return self.unlocked == False
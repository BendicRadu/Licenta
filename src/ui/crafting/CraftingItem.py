class CraftingItem:

    # crafting_items_required map
    # with key = tile_code
    # value = quantity
    def __init__(self, tile_code, crafting_items_required):
        self.tile_code = tile_code
        self.crafting_items_required = crafting_items_required



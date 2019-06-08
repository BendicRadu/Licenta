from ui.inventory.RenderInventory import RenderInventory


class InventoryManager:

    def __init__(self, render_inventory: RenderInventory):
        self.render_inventory = render_inventory

    def select_item(self, mouse_pos):
        self.render_inventory.select_item(mouse_pos)

    def get_selected_item_sprite(self, selected_pos):
        return self.render_inventory.get_selected_item_sprite(selected_pos)

    def get_selected_pos(self):
        return self.render_inventory.get_selected_pos()

    def get_inventory_sprites(self):
        return self.render_inventory.get_sprites()

    def get_quantity_sprites(self):
        return self.render_inventory.get_quantity_sprites()



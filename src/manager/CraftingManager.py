from ui.crafting.RenderCrafting import RenderCrafting
from ui.inventory.RenderInventory import RenderInventory
from util import GameVars


class CraftingManager:

    def __init__(self, render_crafting: RenderCrafting, render_inventory: RenderInventory):

        # TODO Replace with constructor params

        self.render_crafting  = render_crafting
        self.render_inventory = render_inventory

        self.inventory_update_events = []
        self.required_items_update_events = []


    def select_crafting_recepie(self, mouse_pos):
        self.render_crafting.select_item(mouse_pos)
        self.required_items_update_events.append(self.render_crafting.get_required_items_update_event())

    def craft_selected(self):

        added_pos = self.render_crafting.craft_selected()

        if added_pos is not None:

            for i in range(0, GameVars.INVENTORY_MATRIX_HEIGHT):
                for j in range(0, GameVars.INVENTORY_MATRIX_WIDTH):

                    event = self.render_inventory.get_item_update_event((i, j))
                    self.inventory_update_events.append(event)

    def get_selected_pos(self):
        return self.render_crafting.get_selected_pos()

    def get_selected_item_sprite(self, selected_pos):
        return self.render_crafting.get_selected_item_sprite(selected_pos)

    def get_crafting_sprites(self):
        return self.render_crafting.get_sprites()

    def get_blank_required_items(self):
        return self.render_crafting.get_blank_required_items()

    def can_craft_selected(self):
        return self.render_crafting.can_craft_selected()

    def get_selected_required_items_sprites(self):
        return self.render_crafting.get_selected_required_items_sprites()

    def get_selected_required_items_sprites_quantities(self):
        return self.get_selected_required_items_sprites_quantities()

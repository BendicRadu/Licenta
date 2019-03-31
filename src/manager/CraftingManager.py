from util import Constants


class CraftingManager:

    def __init__(self, render_crafting, render_inventory):

        # TODO Replace with constructor params

        self.render_crafting  = render_crafting
        self.render_inventory = render_inventory

        self.inventory_update_events = []
        self.required_items_update_events = []


    def select_crafting_recepie(self, mouse_pos):
        self.render_crafting.select_item(mouse_pos)
        self.required_items_update_events.append(self.render_crafting.get_required_items_update_event())
        return self.render_crafting.select_item(mouse_pos)


    def craft_selected(self):

        added_pos = self.render_crafting.craft_selected()

        if added_pos is not None:

            for i in range(0, Constants.INVENTORY_MATRIX_HEIGHT):
                for j in range(0, Constants.INVENTORY_MATRIX_WIDTH):

                    event = self.render_inventory.get_item_update_event((i, j))
                    self.inventory_update_events.append(event)

from maps.RenderMap.RenderMap import RenderMap
from ui.inventory.RenderInventory import RenderInventory
from util import Constants


class WorldChangeManager:

    def __init__(self, render_map, render_inventory):

        # TODO Replace with constructor params

        self.render_map = render_map
        self.render_inventory = render_inventory


    def is_selected_tile_in_range_of_player(self, mouse_pos_raw):

        selected_tile = self.render_map.get_selected_tile(mouse_pos_raw)
        tile_under_player = self.render_map.get_tile_under_player()

        print(selected_tile.i, selected_tile.j, " ", tile_under_player.i, tile_under_player.j)

        is_in_reach_x = abs(selected_tile.j - tile_under_player.j) <= 1
        is_in_reach_y = abs(selected_tile.i - tile_under_player.i) <= 1

        is_not_under_player = not (selected_tile.i == tile_under_player.i and selected_tile.j == tile_under_player.j)

        return is_in_reach_x and is_in_reach_y and is_not_under_player

    def update_tile(self, mouse_pos_raw):

        if not self.is_selected_tile_in_range_of_player(mouse_pos_raw):
            return

        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        if tile.tile_code in Constants.TILES_BUILDABLE:
            self.place_tile(mouse_pos_raw)

        else:
            self.break_tile(mouse_pos_raw)


    def break_tile(self, mouse_pos_raw):

        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        # Can't break buildable tiles (Grass, dirt, etc)
        if tile.tile_code in Constants.TILES_BUILDABLE:
            return

        print(tile.tile_code)

        self.render_map.remove_selected_tile(mouse_pos_raw)
        print(self.render_inventory.auto_add_item(tile.tile_code, 1))


    def place_tile(self, mouse_pos_raw):

        if not self.render_inventory.is_item_selected():
            return

        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        # Can only place new tiles on top of buildable ones
        if tile.tile_code not in Constants.TILES_BUILDABLE:
            return

        item = self.render_inventory.get_selected_item()

        # If no item is selected
        if item.tile_code == '-1':
            return

        self.render_map.place_on_selected_tile(mouse_pos_raw, item.tile_code)
        self.render_inventory.take_one_selected_item()


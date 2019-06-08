import pygame

from maps.RenderMap.RenderMap import RenderMap
from sprites.HpRect import HpRect
from ui.crafting.RenderCrafting import RenderCrafting
from ui.inventory.RenderInventory import RenderInventory
from util import GameVars
from util.Singleton import Singleton


class WorldChangeManager:

    def __init__(self, render_map: RenderMap, render_inventory: RenderInventory, render_crafting: RenderCrafting):

        self.render_map = render_map
        self.render_inventory = render_inventory
        self.render_crafting  = render_crafting

        self.inventory_update_events = []
        self.crafting_update_events = []

        # This is used so a tile doesn't break instantly
        self.tile_to_break = None
        self.tile_to_break_thoughness = None
        # This is used to signal that the player started breaking a tile last frame
        self.is_breaking = False

    def is_selected_tile_in_range_of_player(self, mouse_pos_raw):

        selected_tile = self.render_map.get_selected_tile(mouse_pos_raw)
        tile_under_player = self.render_map.get_tile_under_player()

        is_in_reach_x = abs(selected_tile.j - tile_under_player.j) <= 1
        is_in_reach_y = abs(selected_tile.i - tile_under_player.i) <= 1

        is_not_under_player = not (selected_tile.i == tile_under_player.i and selected_tile.j == tile_under_player.j)

        return is_in_reach_x and is_in_reach_y and is_not_under_player

    def is_selected_tile_breakable(self, mouse_pos_raw):
        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        return tile.tile_code in GameVars.TILES_BREAKABLE


    def break_tile(self, mouse_pos_raw):

        # TODO Refactor

        if not self.is_selected_tile_in_range_of_player(mouse_pos_raw):
            return

        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        if tile.tile_code in GameVars.TILES_BUILDABLE:
            self.__reset_tile_to_break()
            return

        self.is_breaking = True

        if self.tile_to_break != tile:
            self.tile_to_break = tile
            self.tile_to_break_thoughness = GameVars.TILE_HIT_POINTS[tile.tile_code]
            self.is_breaking = True

        self.tile_to_break_thoughness -= 1

        if self.tile_to_break_thoughness <= 0:

            self.__reset_tile_to_break()

            self.render_map.remove_selected_tile(mouse_pos_raw)

            if tile.tile_code in GameVars.TILES_THAT_GROW:
                self.render_map.remove_growing_tile(mouse_pos_raw)

            # Player has unlocked a new item (Crafting chests are not added to the inventory)
            if tile.tile_code == GameVars.TileCode.CRAFTING_CHEST.value:
                event = self.render_crafting.unlock_next_item()
                self.crafting_update_events.append(event)

            else:

                items_to_be_added = GameVars.TILES_ITEM_MAP[tile.tile_code]

                for item_tile_code in items_to_be_added:

                    added_pos = self.render_inventory.auto_add_item(item_tile_code, 1)
                    event = self.render_inventory.get_item_update_event(added_pos)
                    self.inventory_update_events.append(event)


    def place_tile(self, mouse_pos_raw):

        self.__reset_tile_to_break()

        if not self.is_selected_tile_in_range_of_player(mouse_pos_raw):
            return

        tile = self.render_map.get_selected_tile(mouse_pos_raw)

        if not self.render_inventory.is_item_selected():
            return

        # Can only place new tiles on top of buildable ones
        if tile.tile_code not in GameVars.TILES_BUILDABLE:
            return


        item = self.render_inventory.get_selected_item()

        if item.tile_code not in GameVars.ITEMS_PLACEABLE:
            return

        if item.tile_code in GameVars.TILES_THAT_GROW:
            self.render_map.add_growing_tile(mouse_pos_raw, item.tile_code)

        # If no item is selected
        if item.tile_code == '-1':
            return

        self.render_map.place_on_selected_tile(mouse_pos_raw, item.tile_code)
        event = self.render_inventory.take_one_selected_item()

        self.inventory_update_events.append(event)


    def __reset_tile_to_break(self):
        self.tile_to_break = None
        self.tile_to_break_thoughness = None
        self.is_breaking = False


    def get_tile_to_break_hp_rects(self):

        if self.tile_to_break is None:
            return

        tile_to_break = self.tile_to_break

        i = tile_to_break.i
        j = tile_to_break.j

        tile_code = tile_to_break.tile_code

        x, y = self.render_map.get_top_left_xy_from_ij(i, j)
        y += GameVars.TILE_SIZE - 5

        total_hp = GameVars.TILE_HIT_POINTS[tile_code]
        remaining_hp = total_hp - self.tile_to_break_thoughness

        return HpRect(x, y, remaining_hp, total_hp)

    def frame_start(self):
        self.is_breaking = False

    def frame_end(self):
        if not self.is_breaking:
            self.__reset_tile_to_break()

    def get_screen_sprites(self):
        return self.render_map.get_sprites()

    def get_selected_tile_sprite(self, mouse_pos):
        return self.render_map.get_selected_tile_sprite(mouse_pos)

    def re_apply_effects(self):
        self.render_map.re_apply_effects()

from util.Singleton import Singleton


class GameStateManager:

    def __init__(self, render_map, render_inventory, render_crafting):
        self.render_map = render_map
        self.render_inventory = render_inventory
        self.render_crafting = render_crafting

    def save(self):
        player_coords = self.render_map.get_player_coords()
        crafting_items = self.render_crafting.get_crafting_items_no()
        camera_coords = self.render_map.get_camera_coords()

        Singleton.player_stats.save(player_coords, crafting_items, camera_coords)

        self.render_inventory.save()

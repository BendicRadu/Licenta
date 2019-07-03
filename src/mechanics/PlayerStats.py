import json

from util.GameVars import BASE_PATH


class PlayerStats:

    PLAYER_STATS_FILE_PATH = BASE_PATH + "resources\\player-stats.json"
    PLAYER_STATS_ORIGINAL_FILE_PATH = BASE_PATH + "resources\\player-stats.json"


    def __init__(self):
        try:
            with open(self.PLAYER_STATS_FILE_PATH, 'r') as file:
                data = file.read()

        except OSError:
            with open(self.PLAYER_STATS_ORIGINAL_FILE_PATH, 'r') as file:
                data = file.read()


        obj = json.loads(data)

        self.crafting_items_no = int(obj["crafting_items_no"])
        self.global_player_x   = int(obj["global_player_x"])
        self.global_player_y   = int(obj["global_player_y"])
        self.player_hunger     = int(obj["player_hunger"])
        self.camera_offset_x   = int(obj["camera_offset_x"])
        self.camera_offset_y   = int(obj["camera_offset_y"])

    def save(self, player_coords, crafting_items, camera_coords):

        data = {
                "crafting_items_no": str(crafting_items),
                "global_player_x":   str(player_coords[0]),
                "global_player_y":   str(player_coords[1]),
                "player_hunger":     str(self.player_hunger),
                "camera_offset_x":   str(camera_coords[0]),
                "camera_offset_y":   str(camera_coords[1])
               }

        with open(self.PLAYER_STATS_FILE_PATH, 'w') as outfile:
            json.dump(data, outfile, indent=4)

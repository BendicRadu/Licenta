class MovementManager:

    def __init__(self, render_map):
        self.render_map = render_map

    def get_player_auto_move(self):
        return self.render_map.get_player_auto_move()

    def get_move_list_to_tile(self, mouse_pos):
        return self.render_map.get_move_list_to_tile(mouse_pos)

    def move_player(self, direction):
        self.render_map.move_player(direction)

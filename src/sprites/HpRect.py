import pygame

from util import Constants


class HpRect:

    def __init__(self, x, y, remaning_hp, total_hp):
        self.x = x
        self.y = y
        self.remaining_hp = remaning_hp
        self.total_hp = total_hp

    def get_hp_left_rect(self):
        remaining_hp_sprite_widh = self.remaining_hp * Constants.TILE_SIZE / self.total_hp
        return pygame.Rect(self.x + 1, self.y, remaining_hp_sprite_widh - 2, Constants.HP_BOX_HEIGHT)

    def get_hp_total_rect(self):
        return pygame.Rect(self.x + 1, self.y, Constants.TILE_SIZE - 2, Constants.HP_BOX_HEIGHT)


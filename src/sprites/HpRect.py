import pygame

from util import GameVars


class HpRect:

    def __init__(self, x, y, remaning_hp, total_hp):
        self.x = x
        self.y = y
        self.remaining_hp = remaning_hp
        self.total_hp = total_hp

    def get_hp_left_rect(self):
        remaining_hp_sprite_widh = self.remaining_hp * GameVars.TILE_SIZE / self.total_hp
        return pygame.Rect(self.x + 1, self.y, remaining_hp_sprite_widh - 2, GameVars.HP_BOX_HEIGHT)

    def get_hp_total_rect(self):
        return pygame.Rect(self.x + 1, self.y, GameVars.TILE_SIZE - 2, GameVars.HP_BOX_HEIGHT)


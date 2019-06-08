import pygame

from util import GameVars


class HungerBar:

    def __init__(self, x, y, current_hunger, total_hunger):
        self.x = x
        self.y = y
        self.current_hunger = current_hunger
        self.total_hunger = total_hunger

    def get_hunger_left_rect(self):
        remaining_hunger_rect_width = self.current_hunger * GameVars.HUNGER_BAR_WIDTH / self.total_hunger
        return pygame.Rect(self.x, self.y, remaining_hunger_rect_width, GameVars.HUNGER_BAR_HEIGHT)

    def get_hunger_total_rect(self):
        return pygame.Rect(self.x, self.y, GameVars.HUNGER_BAR_WIDTH, GameVars.HUNGER_BAR_HEIGHT)


    def get_total_hunger_xy(self):
        return self.x + (GameVars.HUNGER_BAR_WIDTH // 2) - 15, self.y

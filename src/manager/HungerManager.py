import datetime
import time

from domain.Exceptions import PlayerStarvedException
from sprites.HungerBar import HungerBar
from ui.inventory.RenderInventory import RenderInventory
from util import Constants
from util.Singleton import Singleton


class HungerManager:

    def __init__(self, render_inventory: RenderInventory):
        self.player_stats = Singleton.player_stats
        self.render_inventory = render_inventory
        self.last_tick_timestamp = datetime.datetime.fromtimestamp(round(time.time()))
        self.inventory_update_events = []

    def eat(self, mouse_pos):

        item = self.render_inventory.get_item_by_mouse_pos(mouse_pos)

        if item.is_empty_cell() or item.tile_code not in Constants.FOOD_ITEMS:
            return


        self.player_stats.player_hunger += Constants.FOOD_VALUES[item.tile_code]


        if self.player_stats.player_hunger > 100:
            self.player_stats.player_hunger = 100

        inventory_update_event = self.render_inventory.take_one_item(mouse_pos)
        self.inventory_update_events.append(inventory_update_event)

    def hunger_tick(self):

        current_time = datetime.datetime.now()
        time_diff = current_time - self.last_tick_timestamp
        minute_diff = time_diff.total_seconds() // 60

        if minute_diff > Constants.HUNGER_TICK_DURATION:

            if self.player_stats.player_hunger - Constants.HUNGER_TICK_VALUE <= 0:
                raise PlayerStarvedException()

            self.player_stats.player_hunger -= 10
            self.last_tick_timestamp = current_time


    def get_hunger_bar_sprite(self):
        hunger_left = self.player_stats.player_hunger
        hunger_total = 100
        x = Constants.HUNGER_BAR_X
        y = Constants.HUNGER_BAR_Y

        return HungerBar(x, y, hunger_left, hunger_total)

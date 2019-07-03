import pygame

from domain.Exceptions import GameOverException, PlayerQuitException
from drawEngine.DrawEngine import DrawEngine
from eventHandler.PlayerEventHandler import PlayerEventHandler
from manager.CraftingManager import CraftingManager
from manager.GameStateManager import GameStateManager
from manager.HungerManager import HungerManager
from manager.InventoryManager import InventoryManager
from manager.MovementManager import MovementManager
from manager.WorldChangeManager import WorldChangeManager
from maps.RenderMap.RenderMap import RenderMap
from ui.crafting.RenderCrafting import RenderCrafting
from ui.inventory.RenderInventory import RenderInventory
from drawEngine.ImageLoader import ImageLoader


class MainLoop:

    def __init__(self):

        pygame.init()

        render_map = RenderMap()
        render_inventory = RenderInventory()
        render_crafting = RenderCrafting()

        world_change_manager = WorldChangeManager(render_map, render_inventory, render_crafting)
        crafting_manager = CraftingManager(render_crafting, render_inventory)
        hunger_manager = HungerManager(render_inventory)
        inventory_manager = InventoryManager(render_inventory)
        movement_manager = MovementManager(render_map)
        image_loader = ImageLoader()

        self.game_state_manager = GameStateManager(render_map, render_inventory, render_crafting)

        self.clock = pygame.time.Clock()

        self.draw_engine = DrawEngine(
            image_loader,
            world_change_manager,
            hunger_manager,
            crafting_manager,
            inventory_manager,
            self.clock
        )

        self.event_handler = PlayerEventHandler(
            world_change_manager,
            crafting_manager,
            hunger_manager,
            inventory_manager,
            movement_manager
        )

    def run(self):

        game_over = False
        self.draw_engine.initial_draw()

        while not game_over:

            try:
                self.event_handler.handle_events()
                self.draw_engine.draw_frame()

                pygame.display.flip()
                self.clock.tick(60)

            except PlayerQuitException:
                self.game_state_manager.save()
                game_over = True

            except GameOverException:
                self.game_state_manager.save()
                game_over = True

        pygame.quit()


main_loop = MainLoop()
main_loop.run()

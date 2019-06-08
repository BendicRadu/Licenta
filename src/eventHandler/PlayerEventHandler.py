import pygame

from domain.Exceptions import PlayerQuitException
from util import GameVars


class PlayerEventHandler:

    def __init__(self,
                 world_change_manager,
                 crafting_manager,
                 hunger_manager,
                 inventory_manager,
                 movement_manager
                 ):

        self.movement_manager = movement_manager
        self.inventory_manager = inventory_manager
        self.world_change_manager = world_change_manager
        self.crafting_manager = crafting_manager
        self.hunger_manager = hunger_manager

        # List of automatic player moves
        self.player_move_list = []
        self.prev_auto_move_1 = None
        self.prev_auto_move_2 = None

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        self.place_tile_pressed = False
        self.break_tile_pressed = False


    def handle_events(self):

        self.hunger_manager.hunger_tick()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    self.up_pressed = True

                if event.key == pygame.K_s:
                    self.down_pressed = True

                if event.key == pygame.K_a:
                    self.left_pressed = True

                if event.key == pygame.K_d:
                    self.right_pressed = True

                if event.key == pygame.K_ESCAPE:
                    raise PlayerQuitException()


            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_w:
                    self.up_pressed = False

                if event.key == pygame.K_s:
                    self.down_pressed = False

                if event.key == pygame.K_a:
                    self.left_pressed = False

                if event.key == pygame.K_d:
                    self.right_pressed = False


            elif event.type == pygame.MOUSEBUTTONDOWN:

                if GameVars.GAME_SCREEN_RECT.collidepoint(mouse_pos):

                    # If tile is in range, place or break depending on mouse button
                    if self.world_change_manager.is_selected_tile_in_range_of_player(mouse_pos):

                        # left mouse button (break tile)
                        if event.button == 1:
                            if self.world_change_manager.is_selected_tile_breakable(mouse_pos):
                                self.break_tile_pressed = True
                            else:
                                self.player_move_list = self.movement_manager.get_move_list_to_tile(mouse_pos)


                        # right mouse button (place tile)
                        elif event.button == 3:
                            self.world_change_manager.place_tile(mouse_pos)


                    # If not in range, move to tile
                    else:
                        if event.button == 1:
                            self.player_move_list = self.movement_manager.get_move_list_to_tile(mouse_pos)

                elif GameVars.INVENTORY_RECT.collidepoint(mouse_pos):

                    if event.button == 1:
                        self.inventory_manager.select_item(mouse_pos)

                    elif event.button == 3:
                        self.hunger_manager.eat(mouse_pos)

                elif GameVars.CRAFTING_RECT.collidepoint(mouse_pos):
                    self.crafting_manager.select_crafting_recepie(mouse_pos)

                elif GameVars.CRAFT_BUTTON_RECT.collidepoint(mouse_pos):
                    self.crafting_manager.craft_selected()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.break_tile_pressed = False
                self.place_tile_pressed = False

        dx, dy = 0, 0

        if self.up_pressed:
            dy = -GameVars.PLAYER_SPEED
            dx = 0

        if self.down_pressed:
            dy = GameVars.PLAYER_SPEED
            dx = 0

        if self.left_pressed:
            dx = -GameVars.PLAYER_SPEED
            dy = 0

        if self.right_pressed:
            dx = GameVars.PLAYER_SPEED
            dy = 0

        if dx != 0 or dy != 0:
            self.player_move_list = []

            direction = (dx, dy)
            auto_move = self.get_player_auto_move()

            if auto_move is not None:
                direction = GameVars.speed_vector_diff(direction, auto_move)

            self.movement_manager.move_player(direction)

        else:
            auto_move = self.get_player_auto_move()

            if auto_move is not None:
                self.player_move_list = [auto_move]

        self.auto_move_player()

        if self.break_tile_pressed:
            self.world_change_manager.break_tile(mouse_pos)

        self.world_change_manager.frame_end()


    def get_player_auto_move(self):

        speed_vector = self.movement_manager.get_player_auto_move()

        if speed_vector is None:
            return None

        if self.prev_auto_move_1 is not None and self.prev_auto_move_2 is not None:

            if self.prev_auto_move_2 == self.prev_auto_move_1 == speed_vector:
                auto_move = self.prev_auto_move_1

            elif self.prev_auto_move_2 == self.prev_auto_move_1 != speed_vector:
                auto_move = self.prev_auto_move_1

            elif self.prev_auto_move_2 != self.prev_auto_move_1 == speed_vector:
                auto_move = speed_vector

            else:
                auto_move = speed_vector

        elif self.prev_auto_move_1 is not None:

            if self.prev_auto_move_1 == speed_vector:
                auto_move = self.prev_auto_move_1
            else:
                auto_move = speed_vector

        else:
            auto_move = speed_vector

        self.prev_auto_move_2 = self.prev_auto_move_1
        self.prev_auto_move_1 = speed_vector

        return auto_move


    def auto_move_player(self):

            if self.player_move_list is not None and len(self.player_move_list) == 0:
                return

            direction = self.player_move_list.pop(0)

            self.movement_manager.move_player(direction)

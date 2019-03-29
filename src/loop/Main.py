import pygame

from manager.CraftingManager import CraftingManager
from manager.WorldChangeManager import WorldChangeManager
from maps.RenderMap.RenderMap import RenderMap
from ui.crafting.RenderCrafting import RenderCrafting
from ui.inventory.RenderInventory import RenderInventory
from util import Constants
from util.Singleton import Singleton


class MainLoop:

    def __init__(self):

        self.render_map       = RenderMap()
        self.render_inventory = RenderInventory()
        self.render_crafting  = RenderCrafting()

        self.world_change_manager = WorldChangeManager(self.render_map, self.render_inventory)
        self.crafting_manager     = CraftingManager(self.render_crafting, self.render_inventory)

        # List of automatic player moves
        self.player_move_list = []

        self.player = Singleton.player

        self.screen = pygame.display.set_mode(
            (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT),
            pygame.FULLSCREEN | pygame.DOUBLEBUF
        )

        self.screen.set_alpha(None)


        self.game_screen = pygame.Surface(
            (Constants.GAME_SCREEN_WIDTH, Constants.GAME_SCREEN_HEIGHT)
        )

        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.font.init()
        Singleton.imageLoader.pygame_init()

        self.font = pygame.font.SysFont('arial', 30)
        self.ui_font = pygame.font.SysFont('arial', 15)
        self.ui_font.set_bold(True)

        self.selected_inventory_pos = None
        self.selected_crafting_pos  = None

        self.show_inventory = True

    def run(self):

        game_over = False

        up_pressed = False
        down_pressed = False
        right_pressed = False
        left_pressed = False

        #self.draw_ui()
        self.draw_initial_inventory()
        self.draw_initial_crafting()
        self.draw_initial_required_items()

        self.draw_crafting_button()

        while not game_over:

            mouse_pos = pygame.mouse.get_pos()


            self.draw_tile_sprites()
            self.draw_selected_tile()
            self.draw_player()
            self.draw_game_screen()

            self.draw_crafting()

            self.draw_required_items()
            self.draw_crafting_button_border()

            self.update_inventory()

            self.auto_move_player()

            self.draw_selected_inventory_item()
            self.draw_selected_crafting_item()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        up_pressed = True

                    if event.key == pygame.K_s:
                        down_pressed = True

                    if event.key == pygame.K_a:
                        left_pressed = True

                    if event.key == pygame.K_d:
                        right_pressed = True

                    if event.key == pygame.K_ESCAPE:
                        game_over = True

                    if event.key == pygame.K_SPACE:

                        # TODO Make propper event

                        self.world_change_manager.update_tile(pygame.mouse.get_pos())


                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_w:
                        up_pressed = False

                    if event.key == pygame.K_s:
                        down_pressed = False

                    if event.key == pygame.K_a:
                        left_pressed = False

                    if event.key == pygame.K_d:
                        right_pressed = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    if self.game_screen.get_rect().collidepoint(mouse_pos):
                        self.player_move_list = self.render_map.get_move_list_to_tile(mouse_pos)

                    elif Constants.INVENTORY_RECT.collidepoint(mouse_pos):
                        self.selected_inventory_pos = self.render_inventory.select_item(mouse_pos)

                    elif Constants.CRAFTING_RECT.collidepoint(mouse_pos):
                        self.selected_crafting_pos = self.render_crafting.select_item(mouse_pos)

                    elif Constants.CRAFT_BUTTON_RECT.collidepoint(mouse_pos):
                        self.crafting_manager.craft_selected()


            dx, dy = 0, 0

            if up_pressed:
                dy = -Constants.PLAYER_SPEED
                dx = 0

            if down_pressed:
                dy = Constants.PLAYER_SPEED
                dx = 0

            if left_pressed:
                dx = -Constants.PLAYER_SPEED
                dy = 0

            if right_pressed:
                dx = Constants.PLAYER_SPEED
                dy = 0

            if dx != 0 or dy != 0:
                self.player_move_list = []
                self.render_map.move_player((dx, dy))


            pygame.display.flip()
            self.clock.tick(90)

    pygame.quit()



    def draw_tile_sprites(self):

        sprites = self.render_map.get_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.TILE_SIZE, Constants.TILE_SIZE)

            self.game_screen.blit(Singleton.imageLoader.load_world_image(sprite.tile_code), rect)

    def draw_selected_inventory_item(self):

        if self.selected_inventory_pos is None:
            return

        selected_cell = self.render_inventory.get_selected_item_sprite(self.selected_inventory_pos)

        if selected_cell is None:
            return

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(selected_cell.x, selected_cell.y,
                                     Constants.INVENTORY_CELL_SIZE, Constants.INVENTORY_CELL_SIZE),
                         1)

    def draw_selected_crafting_item(self):

        if self.selected_crafting_pos is None:
            return

        selected_cell = self.render_crafting.get_selected_item_sprite(self.selected_crafting_pos)

        if selected_cell is None:
            return

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(selected_cell.x, selected_cell.y,
                                     Constants.CRAFTING_CELL_SIZE, Constants.CRAFTING_CELL_SIZE),
                         1)

    def draw_selected_tile(self):

        mouse_pos = pygame.mouse.get_pos()

        is_selected_reachable = self.world_change_manager\
            .is_selected_tile_in_range_of_player(mouse_pos)

        color = (0, 0, 0)

        if is_selected_reachable:
            color = (0, 255, 0)

        selected_tile = self.render_map.get_selected_tile_sprite(mouse_pos)

        pygame.draw.rect(self.game_screen, color,
                         pygame.Rect(selected_tile.x, selected_tile.y, Constants.TILE_SIZE, Constants.TILE_SIZE),
                         2)

        self.draw_selected_tile_name(selected_tile.tile_code)


    def draw_selected_tile_name(self, tile_code):

        text = Constants.TileCode.get_description(tile_code)

        text_surface = self.font.render(str(self.clock.get_fps()), False, (0, 0, 0))
        self.game_screen.blit(text_surface, (10, 0))

    def draw_player(self):

        rect = pygame.Rect(Constants.PLAYER_SCREEN_X, Constants.PLAYER_SCREEN_Y,
                           Constants.PLAYER_SIZE, Constants.PLAYER_SIZE),

        self.game_screen.blit(Singleton.imageLoader.load_player_image(self.player.direction), rect)

    def draw_game_screen(self):

        # TODO move all the _draw methods related to the game screen here

        game_screen_rect = pygame.Rect(0, 0, Constants.GAME_SCREEN_WIDTH, Constants.GAME_SCREEN_HEIGHT)
        self.screen.blit(self.game_screen, game_screen_rect)

    def draw_ui(self):

        rect = pygame.Rect(Constants.GAME_SCREEN_WIDTH, 0,
                           Constants.UI_WIDTH, Constants.UI_HEIGHT),

        self.screen.blit(Singleton.imageLoader.ui_background, rect)

    def draw_initial_inventory(self):

        sprites = self.render_inventory.get_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.INVENTORY_CELL_SIZE, Constants.INVENTORY_CELL_SIZE)

            self.screen.blit(Singleton.imageLoader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Inventory", False, (255, 255, 255))
        self.screen.blit(text_surface, Constants.INVENTORY_TEXT_TOP_LEFT)

        self.__draw_quantities()

    def draw_initial_crafting(self):
        sprites = self.render_crafting.get_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.CRAFTING_CELL_SIZE, Constants.CRAFTING_CELL_SIZE)

            self.screen.blit(Singleton.imageLoader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Crafting recipes", False, (255, 255, 255))
        self.screen.blit(text_surface, Constants.CRAFTING_TEXT_TOP_LEFT)

        self.__draw_quantities()

    def draw_initial_required_items(self):

        sprites = self.render_crafting.get_blank_required_items()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.REQUIRED_ITEMS_CELL_SIZE, Constants.REQUIRED_ITEMS_CELL_SIZE)

            self.screen.blit(Singleton.imageLoader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Items required for crafting", False, (255, 255, 255))
        self.screen.blit(text_surface, Constants.REQUIRED_ITEMS_TEXT_TOP_LEFT)


    def __draw_quantities(self):

        sprites = self.render_inventory.get_quantity_sprites()

        for sprite in sprites:

            text_surface = self.ui_font.render(sprite.text, False, (255, 255, 255))
            self.screen.blit(text_surface, (sprite.x, sprite.y))

    def draw_crafting_button(self):

        rect = Constants.CRAFT_BUTTON_RECT
        self.screen.blit(Singleton.imageLoader.load_inventory_image('1'), rect)

        text_surface = self.ui_font.render("Craft!", False, (255, 255, 255))
        self.screen.blit(text_surface, Constants.CRAFT_BUTTON_TEXT_TOP_LEFT)

    def draw_crafting_button_border(self):

        color = (0, 0, 0)

        if Constants.CRAFT_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
            if self.render_crafting.can_craft_selected():
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

        pygame.draw.rect(self.screen, color, Constants.CRAFT_BUTTON_RECT, 2)


    def draw_required_items(self):

        sprites = self.render_crafting.get_selected_required_items_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.REQUIRED_ITEMS_CELL_SIZE, Constants.REQUIRED_ITEMS_CELL_SIZE)

            self.screen.blit(Singleton.imageLoader.load_inventory_image(sprite.tile_code), rect)

        self.__draw_required_items_quantities()

    def __draw_required_items_quantities(self):

        sprites = self.render_crafting.get_selected_required_items_sprites_quantities()

        for sprite in sprites:
            text_surface = self.ui_font.render(sprite.text, False, (255, 255, 255))
            self.screen.blit(text_surface, (sprite.x, sprite.y))

    def draw_crafting(self):

        sprites = self.render_crafting.get_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, Constants.CRAFTING_CELL_SIZE, Constants.CRAFTING_CELL_SIZE)

            # TODO special sprites for crafting

            self.screen.blit(Singleton.imageLoader.load_inventory_image(sprite.tile_code), rect)

    #===================================================================================================================

    def auto_move_player(self):

            if self.player_move_list is not None and len(self.player_move_list) == 0:
                return

            direction = self.player_move_list.pop(0)

            self.render_map.move_player(direction)

    def update_inventory(self):

        update_events  = self.world_change_manager.inventory_update_events
        update_events += self.crafting_manager.inventory_update_events

        self.clear_inventory_events()

        for event in update_events:

            rect = pygame.Rect(event.cell_x, event.cell_y, Constants.INVENTORY_CELL_SIZE, Constants.INVENTORY_CELL_SIZE)
            self.screen.blit(Singleton.imageLoader.load_inventory_image(event.tile_code), rect)

            if event.tile_code == '-1':
                continue

            text_surface = self.ui_font.render(event.quantity, False, (255, 255, 255))
            self.screen.blit(text_surface, (event.text_x, event.text_y))


    #===================================================================================================================

    def clear_inventory_events(self):
        self.world_change_manager.inventory_update_events = []
        self.crafting_manager.inventory_update_events = []


a = MainLoop()
a.run()

import pygame

from util import GameVars
from util.Singleton import Singleton


class DrawEngine:

    def __init__(self,
                 image_loader,
                 world_change_manager,
                 hunger_manager,
                 crafting_manager,
                 inventory_manager,
                 clock
                 ):


        self.inventory_manager = inventory_manager
        self.world_change_manager = world_change_manager
        self.hunger_manager = hunger_manager
        self.crafting_manager = crafting_manager

        self.clock = clock

        self.screen = pygame.display.set_mode(
            (GameVars.SCREEN_WIDTH, GameVars.SCREEN_HEIGHT),
            pygame.DOUBLEBUF | pygame.FULLSCREEN
        )

        self.screen.set_alpha(None)

        self.game_screen = pygame.Surface(
            (GameVars.GAME_SCREEN_WIDTH, GameVars.GAME_SCREEN_HEIGHT)
        )

        pygame.font.init()

        self.font = pygame.font.SysFont('arial', 30)
        self.ui_font = pygame.font.SysFont('arial', 15)
        self.ui_font.set_bold(True)

        self.player = Singleton.player

        image_loader.pygame_init()
        self.image_loader = image_loader



    def initial_draw(self):
        self.draw_initial_inventory()
        self.draw_initial_crafting()
        self.draw_initial_required_items()
        self.draw_crafting_button()

    def draw_frame(self):

        self.world_change_manager.re_apply_effects()

        self.world_change_manager.frame_start()
        self.draw_tile_sprites()
        self.draw_selected_tile()
        self.draw_player()
        self.draw_game_screen()
        self.update_inventory()
        self.update_required_items()
        self.update_crafting()
        self.draw_tile_to_break_hitpoints()
        self.draw_crafting_button_border()
        self.draw_hunger_bar()
        self.draw_ui_grids()
        self.draw_selected_inventory_item()
        self.draw_selected_crafting_item()


    def draw_tile_sprites(self):

        sprites = self.world_change_manager.get_screen_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.TILE_SIZE, GameVars.TILE_SIZE)

            if sprite.tile_code == GameVars.TileCode.NaN:
                self.game_screen.blit(self.image_loader.non_visible_tile, rect)

            else:
                self.game_screen.blit(self.image_loader.load_world_image(sprite.tile_code), rect)

    def draw_selected_inventory_item(self):

        selected_pos = self.inventory_manager.get_selected_pos()

        if selected_pos is None:
            return

        selected_cell = self.inventory_manager.get_selected_item_sprite(selected_pos)

        if selected_cell is None:
            return

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(selected_cell.x + 1, selected_cell.y + 1,
                                     GameVars.INVENTORY_CELL_SIZE + 1, GameVars.INVENTORY_CELL_SIZE + 1),
                         1)

    def draw_selected_crafting_item(self):

        selected_pos = self.crafting_manager.get_selected_pos()

        if selected_pos is None:
            return

        selected_cell = self.crafting_manager.get_selected_item_sprite(selected_pos)

        if selected_cell is None:
            return

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(selected_cell.x + 1, selected_cell.y + 1,
                                     GameVars.CRAFTING_CELL_SIZE + 1, GameVars.CRAFTING_CELL_SIZE + 1),
                         1)

    def draw_selected_tile(self):

        mouse_pos = pygame.mouse.get_pos()

        if not self.game_screen.get_rect().collidepoint(mouse_pos):
            return

        is_selected_reachable = self.world_change_manager \
            .is_selected_tile_in_range_of_player(mouse_pos)

        color = (0, 0, 0)

        if is_selected_reachable:
            color = (0, 255, 0)

        selected_tile = self.world_change_manager.get_selected_tile_sprite(mouse_pos)

        pygame.draw.rect(self.game_screen, color,
                         pygame.Rect(selected_tile.x, selected_tile.y, GameVars.TILE_SIZE, GameVars.TILE_SIZE),
                         2)

        self.draw_selected_tile_name(selected_tile.tile_code)

    def draw_selected_tile_name(self, tile_code):

        text = GameVars.TileCode.get_description(tile_code)

        text_surface = self.font.render(str(self.clock.get_fps()), False, (0, 0, 0))
        self.game_screen.blit(text_surface, (10, 0))

    def draw_player(self):

        rect = pygame.Rect(GameVars.PLAYER_SCREEN_X, GameVars.PLAYER_SCREEN_Y,
                           GameVars.PLAYER_SIZE, GameVars.PLAYER_SIZE),

        self.game_screen.blit(self.image_loader.load_player_image(self.player.direction), rect)

    def draw_game_screen(self):
        game_screen_rect = pygame.Rect(0, 0, GameVars.GAME_SCREEN_WIDTH, GameVars.GAME_SCREEN_HEIGHT)
        self.screen.blit(self.game_screen, game_screen_rect)

    def draw_ui(self):

        rect = pygame.Rect(GameVars.GAME_SCREEN_WIDTH, 0,
                           GameVars.UI_WIDTH, GameVars.UI_HEIGHT),

        self.screen.blit(self.image_loader.ui_background, rect)

    def draw_initial_inventory(self):

        sprites = self.inventory_manager.get_inventory_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.INVENTORY_CELL_SIZE, GameVars.INVENTORY_CELL_SIZE)

            self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Inventory", False, (255, 255, 255))
        self.screen.blit(text_surface, GameVars.INVENTORY_TEXT_TOP_LEFT)

        self.__draw_quantities()

    def draw_initial_crafting(self):
        sprites = self.crafting_manager.get_crafting_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.CRAFTING_CELL_SIZE, GameVars.CRAFTING_CELL_SIZE)

            self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Crafting recipes", False, (255, 255, 255))
        self.screen.blit(text_surface, GameVars.CRAFTING_TEXT_TOP_LEFT)

        self.__draw_quantities()

    def draw_initial_required_items(self):

        sprites = self.crafting_manager.get_blank_required_items()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.REQUIRED_ITEMS_CELL_SIZE,
                               GameVars.REQUIRED_ITEMS_CELL_SIZE)

            self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

        text_surface = self.ui_font.render("Items required for crafting", False, (255, 255, 255))
        self.screen.blit(text_surface, GameVars.REQUIRED_ITEMS_TEXT_TOP_LEFT)

    def __draw_quantities(self):

        sprites = self.inventory_manager.get_quantity_sprites()

        for sprite in sprites:
            text_surface = self.ui_font.render(sprite.text, False, (255, 255, 255))
            self.screen.blit(text_surface, (sprite.x, sprite.y))

    def draw_crafting_button(self):

        rect = GameVars.CRAFT_BUTTON_RECT
        self.screen.blit(self.image_loader.load_inventory_image('craft_btn'), rect)

        text_surface = self.ui_font.render("Craft!", False, (255, 255, 255))
        self.screen.blit(text_surface, GameVars.CRAFT_BUTTON_TEXT_TOP_LEFT)

    def draw_crafting_button_border(self):

        color = (0, 0, 0)

        if GameVars.CRAFT_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
            if self.crafting_manager.can_craft_selected():
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

        pygame.draw.rect(self.screen, color, GameVars.CRAFT_BUTTON_RECT, 2)

    def draw_required_items(self):

        sprites = self.crafting_manager.get_selected_required_items_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.REQUIRED_ITEMS_CELL_SIZE,
                               GameVars.REQUIRED_ITEMS_CELL_SIZE)

            self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

        self.__draw_required_items_quantities()

    def __draw_required_items_quantities(self):

        sprites = self.crafting_manager.get_selected_required_items_sprites_quantities()

        for sprite in sprites:
            text_surface = self.ui_font.render(sprite.text, False, (255, 255, 255))
            self.screen.blit(text_surface, (sprite.x, sprite.y))

    def draw_crafting(self):

        sprites = self.crafting_manager.get_crafting_sprites()

        for sprite in sprites:
            rect = pygame.Rect(sprite.x, sprite.y, GameVars.CRAFTING_CELL_SIZE, GameVars.CRAFTING_CELL_SIZE)

            # TODO special sprites for crafting

            self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

    def draw_tile_to_break_hitpoints(self):

        hp_rect = self.world_change_manager.get_tile_to_break_hp_rects()

        if hp_rect is None:
            return

        remaining_hp_rect = hp_rect.get_hp_left_rect()
        total_hp_rect = hp_rect.get_hp_total_rect()

        pygame.draw.rect(self.screen, (0, 0, 0), total_hp_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), remaining_hp_rect)

    def draw_hunger_bar(self):

        hunger_bar = self.hunger_manager.get_hunger_bar_sprite()

        total_hunger_rect = hunger_bar.get_hunger_total_rect()
        pygame.draw.rect(self.screen, (0, 0, 0), total_hunger_rect)

        remaining_hunger_rect = hunger_bar.get_hunger_left_rect()
        pygame.draw.rect(self.screen, (0, 255, 0), remaining_hunger_rect)

        hunger_text = str(hunger_bar.current_hunger) + "/" + str(hunger_bar.total_hunger)
        text_surface = self.ui_font.render(hunger_text, False, (255, 255, 255))
        self.screen.blit(text_surface, hunger_bar.get_total_hunger_xy())


    # Update -----------------------------------------------------------------------------------------------------------

    def update_inventory(self):

        update_events  = self.world_change_manager.inventory_update_events
        update_events += self.crafting_manager.inventory_update_events
        update_events += self.hunger_manager.inventory_update_events

        self.clear_inventory_events()

        for event in update_events:

            rect = pygame.Rect(event.cell_x, event.cell_y, GameVars.INVENTORY_CELL_SIZE, GameVars.INVENTORY_CELL_SIZE)
            self.screen.blit(self.image_loader.load_inventory_image(event.tile_code), rect)

            if event.tile_code == GameVars.TileCode.NaN.value:
                continue

            text_surface = self.ui_font.render(event.quantity, False, (255, 255, 255))
            self.screen.blit(text_surface, (event.text_x, event.text_y))

    def update_crafting(self):

        update_events  = self.world_change_manager.crafting_update_events
        self.clear_crafting_events()

        for event in update_events:

            rect = pygame.Rect(event.cell_x, event.cell_y, GameVars.CRAFTING_CELL_SIZE, GameVars.CRAFTING_CELL_SIZE)
            self.screen.blit(self.image_loader.load_inventory_image(event.tile_code), rect)



    def update_required_items(self):

        update_events = self.crafting_manager.required_items_update_events
        self.clear_required_items_events()

        for event in update_events:

            self.draw_initial_required_items()

            for sprite in event.required_items_sprites:
                rect = pygame.Rect(sprite.x, sprite.y, GameVars.REQUIRED_ITEMS_CELL_SIZE,
                                   GameVars.REQUIRED_ITEMS_CELL_SIZE)

                self.screen.blit(self.image_loader.load_inventory_image(sprite.tile_code), rect)

            for sprite in event.quantity_sprites:
                text_surface = self.ui_font.render(sprite.text, False, (255, 255, 255))
                self.screen.blit(text_surface, (sprite.x, sprite.y))


    # ===================================================================================================================

    def clear_inventory_events(self):
        self.world_change_manager.inventory_update_events = []
        self.crafting_manager.inventory_update_events = []
        self.hunger_manager.inventory_update_events = []

    def clear_required_items_events(self):
        self.crafting_manager.required_items_update_events = []

    def clear_crafting_events(self):
        self.world_change_manager.crafting_update_events = []



    def draw_ui_grids(self):
        self.draw_inventory_grid()
        self.draw_crafting_grid()


    def draw_inventory_grid(self):

        for i in range(6):
            y1 = i * GameVars.INVENTORY_CELL_SIZE + GameVars.INVENTORY_TOP_LEFT[1]
            x1 = GameVars.INVENTORY_TOP_LEFT[0]

            y2 = y1
            x2 = x1 + GameVars.INVENTORY_SCREEN_WIDTH

            pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2), 2)


        for i in range(7):

            x1 = i * GameVars.INVENTORY_CELL_SIZE + GameVars.INVENTORY_TOP_LEFT[0]
            y1 = GameVars.INVENTORY_TOP_LEFT[1]

            y2 = y1 + GameVars.INVENTORY_SCREEN_HEIGHT
            x2 = x1

            pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2), 2)


    def draw_crafting_grid(self):

        for i in range(6):
            y1 = i * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[1]
            x1 = GameVars.CRAFTING_TOP_LEFT[0]

            y2 = y1
            x2 = x1 + GameVars.CRAFTING_SCREEN_WIDTH

            pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

        for i in range(7):

            x1 = i * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[0]
            y1 = GameVars.CRAFTING_TOP_LEFT[1]

            y2 = y1 + GameVars.CRAFTING_SCREEN_HEIGHT
            x2 = x1

            pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2), 2)








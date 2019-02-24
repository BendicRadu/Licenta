import pygame

from maps.RenderMap.RenderMap import RenderMap
from util import Constants
from util.Singleton import Singleton


class MainLoop:

    def __init__(self):

        self.render_map = RenderMap()

        self.screen = pygame.display.set_mode((Constants.GAME_SCREEN_WIDTH, Constants.GAME_SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.init()

    def run(self):

        background = pygame.Surface(self.screen.get_size())
        background.fill((250, 0, 0))

        game_over = False

        up_pressed = False
        down_pressed = False
        right_pressed = False
        left_pressed = False


        while not game_over:

            self.draw_tile_sprites()
            self.draw_selected_tile()
            self.draw_player()

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
                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_w:
                        up_pressed = False

                    if event.key == pygame.K_s:
                        down_pressed = False

                    if event.key == pygame.K_a:
                        left_pressed = False

                    if event.key == pygame.K_d:
                        right_pressed = False


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
                self.render_map.move_player((dx, dy))

            pygame.display.flip()
            self.clock.tick(5000)

    def draw_rect(self, surface, fill_color, outline_color, rect, border=1):
        surface.fill(outline_color, rect)
        surface.fill(fill_color, rect.inflate(-border * 2, -border * 2))



    def draw_tile_sprites(self):

        sprites = self.render_map.get_sprites()

        for sprite in sprites:

            rect = pygame.Rect(sprite.x, sprite.y, Constants.TILE_SIZE, Constants.TILE_SIZE)

            self.screen.blit(Singleton.imageLoader.load(sprite.tile_code), rect)


    def draw_selected_tile(self):

        selected_tile = self.render_map.get_selected_tile(pygame.mouse.get_pos())

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(selected_tile.x, selected_tile.y, Constants.TILE_SIZE, Constants.TILE_SIZE),
                         2)


    def draw_player(self):

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(Constants.PLAYER_SCREEN_X,
                                     Constants.PLAYER_SCREEN_Y,
                                     Constants.PLAYER_SIZE, Constants.PLAYER_SIZE),
                         0)


a = MainLoop()
a.run()

from sprites.MapSprite import Sprite
from sprites.TextSprite import TextSprite
from ui.crafting.Crafting import Crafting
from util import Constants


class RenderCrafting:

    def __init__(self):
        self.crafting = Crafting()


    def get_sprites(self):

        matrix = self.crafting.get_matrix()

        sprite_list = []

        for i in range(matrix.height):
            for j in range(matrix.width):

                tile_code = matrix[(i, j)].tile_code

                x = j * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[0]
                y = i * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[1]

                sprite = Sprite(x, y, tile_code)

                sprite_list.append(sprite)

        return sprite_list

    def craft_selected(self):
        return self.crafting.craft()

    def can_craft_selected(self):

        if self.get_selected() is None:
            return False

        return self.crafting.can_craft()

    def select_item(self, mouse_pos):

        x, y = mouse_pos

        j = (x - Constants.CRAFTING_TOP_LEFT[0]) // Constants.CRAFTING_CELL_SIZE
        i = (y - Constants.CRAFTING_TOP_LEFT[1]) // Constants.CRAFTING_CELL_SIZE

        return self.crafting.select((i, j))


    def get_selected(self):
        return self.crafting.get_selected()

    def get_selected_item_sprite(self, pos):

        if self.get_selected().is_empty_cell():
            return None

        i, j = pos

        x = j * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[0]
        y = i * Constants.CRAFTING_CELL_SIZE + Constants.CRAFTING_TOP_LEFT[1]

        return Sprite(x, y, None)

    def get_selected_required_items_sprites(self):

        crafting_item = self.crafting.get_selected()

        if crafting_item is None:
            return []

        offset_x = Constants.REQUIRED_ITEMS_TOP_LEFT[0]
        y        = Constants.REQUIRED_ITEMS_TOP_LEFT[1]
        sprites = []

        for required_item in crafting_item.crafting_items_required.keys():

            x = offset_x
            sprite = Sprite(x, y, required_item)

            sprites.append(sprite)

            offset_x += Constants.REQUIRED_ITEMS_CELL_SIZE


        return sprites

    def get_selected_required_items_sprites_quantities(self):

        crafting_item = self.crafting.get_selected()

        if crafting_item is None:
            return []

        offset_x = Constants.REQUIRED_ITEMS_TOP_LEFT[0] + Constants.REQUIRED_ITEMS_CELL_SIZE - 20
        y = Constants.REQUIRED_ITEMS_TOP_LEFT[1] + Constants.REQUIRED_ITEMS_CELL_SIZE - 20
        sprites = []

        for required_item in crafting_item.crafting_items_required.keys():

            quantity = crafting_item.crafting_items_required[required_item]

            x = offset_x
            sprite = TextSprite(x, y, str(quantity))

            sprites.append(sprite)

            offset_x += Constants.REQUIRED_ITEMS_CELL_SIZE

        return sprites


    def get_blank_required_items(self):

        offset_x = Constants.REQUIRED_ITEMS_TOP_LEFT[0]
        y = Constants.REQUIRED_ITEMS_TOP_LEFT[1]
        sprites = []

        width = Constants.REQUIRED_ITEMS_WIDTH

        while len(sprites) < width:

            x = offset_x
            sprite = Sprite(x, y, '-1')

            sprites.append(sprite)

            offset_x += Constants.REQUIRED_ITEMS_CELL_SIZE

        return sprites

    def get_crafting_button_sprite(self):

        x = Constants.CRAFT_BUTTON_TOP_LEFT[0]
        y = Constants.CRAFT_BUTTON_TOP_LEFT[1]

        return Sprite(x, y, '1')

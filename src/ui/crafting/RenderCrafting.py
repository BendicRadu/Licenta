from sprites.MapSprite import Sprite
from sprites.TextSprite import TextSprite
from ui.crafting.Crafting import Crafting
from util import GameVars


class RenderCrafting:

    def __init__(self):
        self.crafting = Crafting()

    def get_crafting_items_no(self):
        return self.crafting.get_crafting_items_no()

    def get_sprites(self):

        matrix = self.crafting.get_matrix()

        sprite_list = []

        for i in range(matrix.height):
            for j in range(matrix.width):

                tile_code = matrix[(i, j)].tile_code

                if tile_code != '-1' and not matrix[i, j].unlocked:
                    tile_code = '1000'

                x = j * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[0]
                y = i * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[1]

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

        j = (x - GameVars.CRAFTING_TOP_LEFT[0]) // GameVars.CRAFTING_CELL_SIZE
        i = (y - GameVars.CRAFTING_TOP_LEFT[1]) // GameVars.CRAFTING_CELL_SIZE

        self.crafting.select((i, j))

    def get_selected_pos(self):
        return self.crafting.selected_pos

    def get_selected(self):
        return self.crafting.get_selected()

    def get_selected_item_sprite(self, pos):

        if self.get_selected().is_empty_cell():
            return None

        i, j = pos

        x = j * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[0]
        y = i * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[1]

        return Sprite(x, y, None)

    def get_selected_required_items_sprites(self):

        crafting_item = self.crafting.get_selected()

        if crafting_item is None:
            return []

        offset_x = GameVars.REQUIRED_ITEMS_TOP_LEFT[0]
        y        = GameVars.REQUIRED_ITEMS_TOP_LEFT[1]
        sprites = []

        for required_item in crafting_item.crafting_items_required.keys():

            x = offset_x
            sprite = Sprite(x, y, required_item)

            sprites.append(sprite)

            offset_x += GameVars.REQUIRED_ITEMS_CELL_SIZE


        return sprites

    def get_selected_required_items_sprites_quantities(self):

        crafting_item = self.crafting.get_selected()

        if crafting_item is None:
            return []

        offset_x = GameVars.REQUIRED_ITEMS_TOP_LEFT[0] + GameVars.REQUIRED_ITEMS_CELL_SIZE - 20
        y = GameVars.REQUIRED_ITEMS_TOP_LEFT[1] + GameVars.REQUIRED_ITEMS_CELL_SIZE - 20
        sprites = []

        for required_item in crafting_item.crafting_items_required.keys():

            quantity = crafting_item.crafting_items_required[required_item]

            x = offset_x
            sprite = TextSprite(x, y, str(quantity))

            sprites.append(sprite)

            offset_x += GameVars.REQUIRED_ITEMS_CELL_SIZE

        return sprites


    def get_blank_required_items(self):

        offset_x = GameVars.REQUIRED_ITEMS_TOP_LEFT[0]
        y = GameVars.REQUIRED_ITEMS_TOP_LEFT[1]
        sprites = []

        width = GameVars.REQUIRED_ITEMS_WIDTH

        while len(sprites) < width:

            x = offset_x
            sprite = Sprite(x, y, '-1')

            sprites.append(sprite)

            offset_x += GameVars.REQUIRED_ITEMS_CELL_SIZE

        return sprites

    def get_crafting_button_sprite(self):

        x = GameVars.CRAFT_BUTTON_TOP_LEFT[0]
        y = GameVars.CRAFT_BUTTON_TOP_LEFT[1]

        return Sprite(x, y, '1')

    def get_required_items_update_event(self):
        return RequiredItemsUpdateEvent(
            self.get_selected_required_items_sprites(),
            self.get_selected_required_items_sprites_quantities()
        )

    def unlock_next_item(self):
        unlocked_pos = self.crafting.unlock_next_item()
        tile_code = self.crafting.get_matrix()[unlocked_pos].tile_code

        i, j = unlocked_pos

        x = j * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[0]
        y = i * GameVars.CRAFTING_CELL_SIZE + GameVars.CRAFTING_TOP_LEFT[1]

        return CraftingUpdateEvent(x, y, tile_code)


# Only happens when unlocking a new item
class CraftingUpdateEvent:

    def __init__(self, cell_x, cell_y, tile_code):
        self.cell_x = cell_x
        self.cell_y = cell_y

        self.tile_code = tile_code


class RequiredItemsUpdateEvent:

    def __init__(self, required_items_sprites, quantity_sprites):

        self.required_items_sprites = required_items_sprites
        self.quantity_sprites = quantity_sprites

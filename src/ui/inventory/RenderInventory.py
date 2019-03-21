from sprites.MapSprite import Sprite
from sprites.TextSprite import TextSprite
from ui.inventory.Inventory import Inventory
from util import Constants
from util.Singleton import Singleton


class RenderInventory:


    def __init__(self):

        self.inventory = Singleton.inventory


    def get_sprites(self):

        matrix = self.inventory.get_matrix()

        sprite_list = []

        for i in range(matrix.height):
            for j in range(matrix.width):
                tile_code = matrix[i, j].tile_code

                x = j * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[0]
                y = i * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[1]

                sprite = Sprite(x, y, tile_code)

                sprite_list.append(sprite)

        return sprite_list

    def get_quantity_sprites(self):

        matrix = self.inventory.get_matrix()

        sprite_list = []

        for i in range(matrix.height):
            for j in range(matrix.width):

                if matrix[i, j].is_empty_cell():
                    continue

                x = j * Constants.INVENTORY_CELL_SIZE \
                    + Constants.INVENTORY_TOP_LEFT[0] \
                    + Constants.INVENTORY_CELL_SIZE // 2 \
                    + Constants.INVENTORY_CELL_SIZE // 6


                y = i * Constants.INVENTORY_CELL_SIZE \
                    + Constants.INVENTORY_TOP_LEFT[1] \
                    + Constants.INVENTORY_CELL_SIZE // 2 \
                    + Constants.INVENTORY_CELL_SIZE // 6

                sprite = TextSprite(x, y, str(matrix[i, j].quantity))

                sprite_list.append(sprite)

        return sprite_list

    def get_selected_item_sprite(self, pos):

        if self.get_selected_item().is_empty_cell():
            return None

        i, j = pos

        x = j * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[0]
        y = i * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[1]

        return Sprite(x, y, None)

    def is_item_selected(self):
        return self.inventory.is_item_selected()

    def take_one_selected_item(self):
        self.get_selected_item().take_one()

        if self.get_selected_item().is_empty():
            self.remove_selected_item()


    def get_selected_item(self):
        return self.inventory.get_selected_item()

    def remove_selected_item(self):
        self.inventory.remove_selected_item()

    def auto_add_item(self, tile_code, quantity):
        return self.inventory.auto_add(tile_code, quantity)

    def select_item(self, mouse_pos):

        x, y = mouse_pos

        j = (x - Constants.INVENTORY_TOP_LEFT[0]) // Constants.INVENTORY_CELL_SIZE
        i = (y - Constants.INVENTORY_TOP_LEFT[1]) // Constants.INVENTORY_CELL_SIZE

        return self.inventory.select((i, j))



from sprites.MapSprite import Sprite
from sprites.TextSprite import TextSprite
from ui.inventory.Inventory import Inventory
from util import Constants
from util.Singleton import Singleton


class RenderInventory:


    def __init__(self):

        self.inventory = Singleton.inventory

    def save(self):
        self.inventory.save()

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

        event = self.get_item_update_event(self.inventory.get_matrix().selected_pos)

        return event

    def get_selected_item(self):
        return self.inventory.get_selected_item()

    def get_item_update_event_by_mouse_pos(self, mouse_pos):
        i, j = mouse_pos

        x = j * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[0]
        y = i * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[1]

        return self.get_item_update_event((i, j))

    def get_item_update_event(self, pos):

        i, j = pos

        cell_x = j * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[0]
        cell_y = i * Constants.INVENTORY_CELL_SIZE + Constants.INVENTORY_TOP_LEFT[1]

        text_x = j * Constants.INVENTORY_CELL_SIZE \
            + Constants.INVENTORY_TOP_LEFT[0] \
            + Constants.INVENTORY_CELL_SIZE // 2 \
            + Constants.INVENTORY_CELL_SIZE // 6

        text_y = i * Constants.INVENTORY_CELL_SIZE \
            + Constants.INVENTORY_TOP_LEFT[1] \
            + Constants.INVENTORY_CELL_SIZE // 2 \
            + Constants.INVENTORY_CELL_SIZE // 6

        item = self.inventory.get_item(pos)

        return InventoryUpdateEvent(cell_x, cell_y, text_x, text_y, item.tile_code, item.quantity)

    def take_one_item(self, mouse_pos):
        x, y = mouse_pos

        j = (x - Constants.INVENTORY_TOP_LEFT[0]) // Constants.INVENTORY_CELL_SIZE
        i = (y - Constants.INVENTORY_TOP_LEFT[1]) // Constants.INVENTORY_CELL_SIZE

        self.get_item((i, j)).take_one()

        if self.get_item((i, j)).is_empty():
            self.remove_item((i, j))

        return self.get_item_update_event((i, j))


    def remove_selected_item(self):
        self.inventory.remove_selected_item()

    def remove_item(self, pos):
        self.inventory.remove_item(pos)

    def auto_add_item(self, tile_code, quantity):
        return self.inventory.auto_add(tile_code, quantity)

    def select_item(self, mouse_pos):

        x, y = mouse_pos

        j = (x - Constants.INVENTORY_TOP_LEFT[0]) // Constants.INVENTORY_CELL_SIZE
        i = (y - Constants.INVENTORY_TOP_LEFT[1]) // Constants.INVENTORY_CELL_SIZE

        return self.inventory.select((i, j))

    def get_item(self, pos):
        return self.inventory.get_item(pos)

    def get_item_by_mouse_pos(self, mouse_pos):
        x, y = mouse_pos

        j = (x - Constants.INVENTORY_TOP_LEFT[0]) // Constants.INVENTORY_CELL_SIZE
        i = (y - Constants.INVENTORY_TOP_LEFT[1]) // Constants.INVENTORY_CELL_SIZE

        return self.inventory.get_item((i, j))


# Holds info about the inventory cell that needs updating
class InventoryUpdateEvent:

    def __init__(self, cell_x, cell_y, text_x, text_y, tile_code, quantity):

        self.cell_x = cell_x
        self.cell_y = cell_y

        self.text_x = text_x
        self.text_y = text_y

        self.quantity = str(quantity)

        if self.quantity == -1:
            self.tile_code = '-1'
        else:
            self.tile_code = tile_code

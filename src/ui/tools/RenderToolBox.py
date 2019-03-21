from sprites.MapSprite import Sprite
from ui.tools.Tools import ToolBox
from util import Constants


class RenderToolbox:

    def __init__(self):
        self.tool_box = ToolBox()

    def get_sprites(self):

        vector = self.tool_box.get_tool_box_vector()

        sprite_list = []

        for i in range(vector.width):

            tile_code = vector[i]

            x = i * Constants.TOOLS_CELL_WIDTH + Constants.TOOLS_TOP_LEFT[0]
            y = Constants.TOOLS_TOP_LEFT[1]

            sprite = Sprite(x, y, tile_code)

            sprite_list.append(sprite)

        return sprite_list

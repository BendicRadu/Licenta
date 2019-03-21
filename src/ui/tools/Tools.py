from util import Constants


class ToolBox:

    def __init__(self):
        self.tool_box_vector = ToolBoxVector()


    def get_tool_box_vector(self):
        return self.tool_box_vector


class ToolBoxVector:


    def __init__(self):

        self.width = Constants.TOOLS_WIDTH
        self.vector = []

        for i in range(self.width):
            # TODO replace with tools sprite
            self.vector.append("0")


    def __getitem__(self, index):
        return self.vector[index]

    def __setitem__(self, index, value):
        self.vector[index] = value

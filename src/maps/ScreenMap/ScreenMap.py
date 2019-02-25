from maps.WorldMap.WorldMap import WorldMap
from sprites.Tile import Tile
from util import Constants
from util.Singleton import Singleton


class ScreenMap:

    def __init__(self, chunk_offset = (5, 5), chunk_pos = Singleton.player.get_local_pos()):

        self.world_map = WorldMap()

        self.player = Singleton.player

        self.current_chunk_offset = chunk_offset
        self.chunk_pos = chunk_pos

        self.matrix = ScreenMapMatrix()
        self.update_tiles()

    def get_tiles(self):
        return self.matrix

    # Get global i and j for the PLAYER
    def get_global_i_j(self, offset_i = 0, offset_j = 0):

        chunk_i = self.current_chunk_offset[0]
        chunk_j = self.current_chunk_offset[1]

        chunk_pos_i = self.chunk_pos[0] + offset_i
        chunk_pos_j = self.chunk_pos[1] + offset_j

        global_i = chunk_i * Constants.CHUNK_SIZE + chunk_pos_i
        global_j = chunk_j * Constants.CHUNK_SIZE + chunk_pos_j

        return global_i, global_j


    def get_updated_chunk_offset(self, x, y):
        return (y // Constants.TILE_SIZE // Constants.CHUNK_SIZE,
                x // Constants.TILE_SIZE // Constants.CHUNK_SIZE)

    def get_updated_chunk_pos(self, x, y):
        return (y // Constants.TILE_SIZE % Constants.CHUNK_SIZE,
                x // Constants.TILE_SIZE % Constants.CHUNK_SIZE)

    def update_tiles(self):

        row_size    = Constants.WIDTH_NO_OF_TILES
        column_size = Constants.HEIGHT_NO_OF_TILES

        base_i, base_j = self.get_global_i_j(-Constants.HEIGHT_NO_OF_TILES // 2, -Constants.WIDTH_NO_OF_TILES // 2)

        for i in range(column_size):
            for j in range(row_size):

                tile = self.world_map.get_tile(base_i + i, base_j + j)
                self.matrix.add_tile(i, j, tile)


    def get_tile_list(self, mouse_pos, camera):

        start_tile = self.get_tile_from_screen(
            Constants.PLAYER_SCREEN_X,
            Constants.PLAYER_SCREEN_Y,
            camera.offset_x, camera.offset_y
        )

        end_tile = self.get_selected_tile(mouse_pos)

        print(end_tile.tile_code)

        if end_tile.tile_code in Constants.TILES_WITH_COLLIDERS:
            return


        start_ij = (start_tile.i, start_tile.j)
        end_ij   = (end_tile.i, end_tile.j)

        return self.matrix.a_start(start_ij, end_ij)



    def get_selected_tile(self, mouse_pos):

        mouse_i = mouse_pos[1] // Constants.TILE_SIZE
        mouse_j = mouse_pos[0] // Constants.TILE_SIZE

        global_i, global_j = self.get_global_i_j(-Constants.HEIGHT_NO_OF_TILES // 2, -Constants.WIDTH_NO_OF_TILES // 2)

        global_mouse_i = global_i + mouse_i
        global_mouse_j = global_j + mouse_j

        tile_code = self.world_map.get_tile(global_mouse_i, global_mouse_j)

        return Tile(mouse_i, mouse_j, tile_code)

    # Returns True if the player was moved
    #         False if the player was not moved
    def move_player(self, direction):

        self.player.move(direction)

        self.current_chunk_offset = self.get_updated_chunk_offset(
            self.player.global_x,
            self.player.global_y
        )

        self.chunk_pos = self.get_updated_chunk_pos(
            self.player.global_x,
            self.player.global_y
        )


        self.update_tiles()

    def get_matrix_tile(self, i, j):
        return self.matrix.get_tile(i, j)

    def get_tile_from_screen(self, base_x, base_y, cam_x, cam_y):

        center_i = (base_y + cam_y) // Constants.TILE_SIZE
        center_j = (base_x + cam_x) // Constants.TILE_SIZE

        return Tile(
            center_i,
            center_j,
            self.matrix.get_tile(center_i, center_j)
        )


class ScreenMapMatrix:

    def __init__(self):
        self.height = Constants.HEIGHT_NO_OF_TILES
        self.width  = Constants.WIDTH_NO_OF_TILES
        self.matrix = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)

            self.matrix.append(row)


    def add_tile(self, i, j, tile):
        self.matrix[i][j] = tile


    def get_tile(self, i, j):
        return self.matrix[i][j]


    def a_start(self, start_ij, end_ij):

        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start_ij)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end_ij)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.matrix) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(self.matrix[len(self.matrix) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.matrix[node_position[0]][node_position[1]] in Constants.TILES_WITH_COLLIDERS:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                if child in closed_list:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


    def __repr__(self):

        estr  = ""
        node = self.parent

        estr += str(self.position)

        while node is not None:
            estr += str(node.position) + "\n"
            node = node.parent

        return estr

    def __eq__(self, other):
        return self.position == other.position

    def get_tile_list(self):

        tile_list = [self.position]

        node = self.parent

        while node is not None:
            tile_list.append(str(node.position))
            node = node.parent

        return tile_list

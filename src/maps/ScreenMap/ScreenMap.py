import time
from abc import abstractmethod

from maps.WorldMap.WorldMap import WorldMap
from sprites.Tile import Tile
from util import GameVars
from util.Singleton import Singleton


class ScreenMap:

    def __init__(self):

        self.world_map = WorldMap()

        self.player = Singleton.player

        self.current_chunk_offset = self.get_chunk_offset()
        self.chunk_pos = self.get_chunk_pos()

        self.tile_growth_service = Singleton.tile_growth_service
        self.counter = 0

        self.matrix = ScreenMapMatrix()
        self.update_tiles()

        self.path_finder = AStar(self.matrix.matrix)

    def get_chunk_offset(self):
        return (self.player.global_y // GameVars.TILE_SIZE // GameVars.CHUNK_SIZE,
                self.player.global_x // GameVars.TILE_SIZE // GameVars.CHUNK_SIZE)

    def get_chunk_pos(self):
        return (self.player.global_y // GameVars.TILE_SIZE % GameVars.CHUNK_SIZE,
                self.player.global_x // GameVars.TILE_SIZE % GameVars.CHUNK_SIZE)

    def get_tiles(self):
        return self.matrix

    # Get global i and j for the PLAYER
    def get_player_global_i_j(self, offset_i=0, offset_j=0):

        chunk_i = self.current_chunk_offset[0]
        chunk_j = self.current_chunk_offset[1]

        chunk_pos_i = self.chunk_pos[0] + offset_i
        chunk_pos_j = self.chunk_pos[1] + offset_j

        global_i = chunk_i * GameVars.CHUNK_SIZE + chunk_pos_i
        global_j = chunk_j * GameVars.CHUNK_SIZE + chunk_pos_j

        return global_i, global_j

    def get_updated_chunk_offset(self, x, y):
        return (y // GameVars.TILE_SIZE // GameVars.CHUNK_SIZE,
                x // GameVars.TILE_SIZE // GameVars.CHUNK_SIZE)

    def get_updated_chunk_pos(self, x, y):
        return (y // GameVars.TILE_SIZE % GameVars.CHUNK_SIZE,
                x // GameVars.TILE_SIZE % GameVars.CHUNK_SIZE)

    def update_tiles(self):

        row_size = GameVars.WIDTH_NO_OF_TILES
        column_size = GameVars.HEIGHT_NO_OF_TILES

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2)

        for i in range(column_size):
            for j in range(row_size):
                tile = self.world_map.get_tile(base_global_i + i, base_global_j + j)
                self.matrix.add_tile(i, j, tile)

        self.apply_effects()

    def _get_buffered_tile_matrix(self, buff_i, buff_j):

        row_size = GameVars.WIDTH_NO_OF_TILES + buff_i * 2
        column_size = GameVars.HEIGHT_NO_OF_TILES + buff_j * 2

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2 - buff_i,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2 - buff_j)

        matrix = []

        for i in range(column_size):

            row = []
            for j in range(row_size):
                tile = self.world_map.get_tile(base_global_i + i, base_global_j + j)
                row.append(tile)

            matrix.append(row)

        return matrix

    def get_tile_list(self, mouse_pos, camera):

        start_tile = self.get_tile_from_screen(
            GameVars.PLAYER_SCREEN_X,
            GameVars.PLAYER_SCREEN_Y,
            camera.offset_x, camera.offset_y
        )

        end_tile = self.get_selected_tile(mouse_pos)

        if end_tile.tile_code in GameVars.TILES_WITH_COLLIDERS:
            return

        start_ij = (start_tile.i, start_tile.j)
        end_ij = (end_tile.i, end_tile.j)

        return self.path_finder.find_path(start_ij, end_ij)

    def get_selected_tile(self, mouse_pos):

        mouse_i = mouse_pos[1] // GameVars.TILE_SIZE
        mouse_j = mouse_pos[0] // GameVars.TILE_SIZE

        tile_code = self.matrix.get_tile(mouse_i, mouse_j)

        return Tile(mouse_i, mouse_j, tile_code)

    def update_selected_tile(self, mouse_pos, tile_code):

        mouse_i = mouse_pos[1] // GameVars.TILE_SIZE
        mouse_j = mouse_pos[0] // GameVars.TILE_SIZE

        global_i, global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                        -GameVars.WIDTH_NO_OF_TILES // 2)

        global_mouse_i = global_i + mouse_i
        global_mouse_j = global_j + mouse_j

        self.world_map.update_tile(global_mouse_i, global_mouse_j, tile_code)
        self.update_tiles()

    def remove_growing_tile(self, mouse_pos):

        mouse_i = mouse_pos[1] // GameVars.TILE_SIZE
        mouse_j = mouse_pos[0] // GameVars.TILE_SIZE

        global_i, global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                        -GameVars.WIDTH_NO_OF_TILES // 2)

        global_mouse_i = global_i + mouse_i
        global_mouse_j = global_j + mouse_j

        self.tile_growth_service.remove_growing_tile((global_mouse_i, global_mouse_j))

    def place_growing_tile(self, mouse_pos, tile_code):

        mouse_i = mouse_pos[1] // GameVars.TILE_SIZE
        mouse_j = mouse_pos[0] // GameVars.TILE_SIZE

        global_i, global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                        -GameVars.WIDTH_NO_OF_TILES // 2)

        global_mouse_i = global_i + mouse_i
        global_mouse_j = global_j + mouse_j

        self.tile_growth_service.add_growing_tile((global_mouse_i, global_mouse_j), tile_code)

    # Returns True if the player was moved
    #         False if the player was not moved
    def move_player(self, direction):

        self.player.move(direction)

        self.current_chunk_offset = self.get_updated_chunk_offset(
            self.player.global_x,
            self.player.global_y
        )

        prev_chunk_pos = self.chunk_pos

        self.chunk_pos = self.get_updated_chunk_pos(
            self.player.global_x,
            self.player.global_y
        )

        diff_i = prev_chunk_pos[0] - self.chunk_pos[0]
        diff_j = prev_chunk_pos[1] - self.chunk_pos[1]

        if abs(diff_i) == GameVars.CHUNK_SIZE - 1 or abs(diff_j) == GameVars.CHUNK_SIZE - 1:
            self.update_tiles()
            self.apply_effects()

        elif diff_i > 0:
            self.move_map_up()
            self.apply_effects()

        elif diff_i < 0:
            self.move_map_down()
            self.apply_effects()

        elif diff_j > 0:
            self.move_map_left()
            self.apply_effects()

        elif diff_j < 0:
            self.move_map_right()
            self.apply_effects()

    def move_map_up(self):
        row_size = GameVars.WIDTH_NO_OF_TILES

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2)

        i = base_global_i
        row = []

        for j in range(row_size):
            row.append(self.world_map.get_tile(i, base_global_j + j))

        del self.matrix.matrix[-1]
        self.matrix.matrix.insert(0, row)

    def move_map_down(self):
        row_size = GameVars.WIDTH_NO_OF_TILES

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2)

        i = base_global_i + GameVars.HEIGHT_NO_OF_TILES - 1

        row = []

        for j in range(row_size):
            row.append(self.world_map.get_tile(i, base_global_j + j))

        del self.matrix.matrix[0]
        self.matrix.matrix.append(row)

    def move_map_left(self):
        column_size = GameVars.HEIGHT_NO_OF_TILES

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2)

        j = base_global_j

        for i in range(column_size):
            del self.matrix.matrix[i][-1]
            self.matrix.matrix[i].insert(0, self.world_map.get_tile(base_global_i + i, j))

    def move_map_right(self):
        column_size = GameVars.HEIGHT_NO_OF_TILES

        base_global_i, base_global_j = self.get_player_global_i_j(-GameVars.HEIGHT_NO_OF_TILES // 2,
                                                                  -GameVars.WIDTH_NO_OF_TILES // 2)

        j = base_global_j + GameVars.WIDTH_NO_OF_TILES - 1

        for i in range(column_size):
            del self.matrix.matrix[i][0]
            self.matrix.matrix[i].append(self.world_map.get_tile(base_global_i + i, j))

    def get_matrix_tile(self, i, j):
        return self.matrix.get_tile(i, j)

    def get_tile_from_screen(self, base_x, base_y, cam_x, cam_y):

        center_i = (base_y + cam_y) // GameVars.TILE_SIZE
        center_j = (base_x + cam_x) // GameVars.TILE_SIZE

        return Tile(
            center_i,
            center_j,
            self.matrix.get_tile(center_i, center_j)
        )

    def apply_effects(self):

        self.counter += 1
        self.counter %= 60

        matrix = self._get_buffered_tile_matrix(1, 1)

        for i in range(1, len(matrix) - 1):
            for j in range(1, len(matrix[0]) - 1):

                if matrix[i][j] == GameVars.TileCode.GRASS.value:
                    continue

                self.apply_growing_tiles_growth(matrix, i, j)

                self.apply_wheat_walls(matrix, i, j)
                self.apply_rock_fog_of_war(matrix, i, j)
                self.apply_rock_walls(matrix, i, j)
                self.apply_animations(matrix, i, j)

    def apply_rock_walls(self, matrix, i, j):

        if self.matrix.get_tile(i - 1, j - 1) == '-1' or (not matrix[i][j] in GameVars.TILES_ORE):
            return

        if matrix[i + 1][j] not in GameVars.TILES_ORE:
            self.matrix.set_tile(i - 1, j - 1, matrix[i][j] + "_1")
        else:
            self.matrix.set_tile(i - 1, j - 1, matrix[i][j] + "_2")

    def apply_wheat_walls(self, matrix, i, j):

        if i == len(self.matrix.matrix):
            return

        if self.matrix.get_tile(i - 1, j - 1) != GameVars.TileCode.WHEAT.value:
            return

        if self.matrix.get_tile(i, j - 1) == GameVars.TileCode.WHEAT.value or \
                self.matrix.get_tile(i, j - 1) == GameVars.TileCode.WHEAT_TOP.value:
            self.matrix.set_tile(i - 1, j - 1, matrix[i][j] + "_3")


    def apply_rock_fog_of_war(self, matrix, i, j):

        # Center
        if not matrix[i][j] in GameVars.TILES_ORE:
            return
        # Top
        elif not matrix[i - 1][j] in GameVars.TILES_ORE:
            return
        # Top left
        elif not matrix[i - 1][j - 1] in GameVars.TILES_ORE:
            return
        # Top right
        elif not matrix[i - 1][j + 1] in GameVars.TILES_ORE:
            return
        # Bot
        elif not matrix[i + 1][j] in GameVars.TILES_ORE:
            return
        # Bot left
        elif not matrix[i + 1][j - 1] in GameVars.TILES_ORE:
            return
        # Bot tight
        elif not matrix[i + 1][j + 1] in GameVars.TILES_ORE:
            return
        # Left
        elif not matrix[i][j - 1] in GameVars.TILES_ORE:
            return
        # Right
        elif not matrix[i][j + 1] in GameVars.TILES_ORE:
            return

        self.matrix.set_tile(i - 1, j - 1, "-1")

    def apply_growing_tiles_growth(self, matrix, i, j):

        # Growing Tiles
        if matrix[i][j] not in GameVars.TILES_THAT_GROW:
            return

        base_global_i, base_global_j = self.get_player_global_i_j(
            -GameVars.HEIGHT_NO_OF_TILES // 2 - 1,
            -GameVars.WIDTH_NO_OF_TILES // 2 - 1)

        global_i = base_global_i + i
        global_j = base_global_j + j

        tile_code = self.tile_growth_service.get_tile_code_for_growth_tile((global_i, global_j))

        self.matrix.set_tile(i - 1, j - 1, tile_code)

    def apply_animations(self, matrix, i, j):

        if matrix[i][j] not in GameVars.TILES_ANIMATED:
            return

        animation_frames = GameVars.TILES_ANIMATION_FRAMES[matrix[i][j]]
        time_per_frame = 60 // animation_frames
        frame = self.counter // time_per_frame

        if frame != 0:

            tile_code = matrix[i][j] + "_" + str(frame)
            self.matrix.set_tile(i - 1, j - 1, tile_code)

        else:
            self.matrix.set_tile(i - 1, j - 1, matrix[i][j])


class ScreenMapMatrix:

    def __init__(self):
        self.height = GameVars.HEIGHT_NO_OF_TILES
        self.width = GameVars.WIDTH_NO_OF_TILES
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

    def set_tile(self, i, j, value):
        self.matrix[i][j] = value


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):

        estr = ""
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


class PathFinder:

    def __init__(self, matrix):
        self.matrix = matrix

    @abstractmethod
    def find_path(self, start_ij, end_ij):
        pass


class AStar(PathFinder):

    def __init__(self, matrix):
        super().__init__(matrix)

    def find_path(self, start_ij, end_ij):

        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        start_time_millis = int(round(time.time() * 1000))

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
                if self.matrix[node_position[0]][node_position[1]] in GameVars.TILES_WITH_COLLIDERS:
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

            current_millis = int(round(time.time() * 1000))

            if current_millis > start_time_millis + 200:
                return None

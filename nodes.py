import pygame
from constants import *
from stacks import Stack


class Node(object):
    def __init__(self, row, column):
        self.debugmode = False

        self.row, self.column = row, column
        self.position = Vector2D(column * TILE_WIDTH, row * TILE_HEIGHT)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        self.portal_node = None
        self.portal_val = 0
        self.home_guide = False
        self.is_home_entrance = False
        self.is_spawn_node = False
        self.is_pacman_start = False
        self.is_ghost_start = False
        self.is_fruit_start = False

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                if self.debugmode:
                    pygame.draw.line(screen, YELLOW, self.position.to_tuple(), self.neighbors[n].position.to_tuple(), 3)
                    pygame.draw.circle(screen, RED, self.position.to_tuple(), 6)


class NodeGroup(object):
    def __init__(self, level):
        self.nodelist = []
        self.homelist = []
        self.level = level
        # self.grid = None
        self.node_stack = Stack()
        self.portalSymbols = ["z"]
        self.pathSymbols = ["p", "P"]
        self.nodeSymbols = ["+", "n", "N", "H", "S", "Y", "F"] + self.portalSymbols
        self.grid = self.read_maze_file(level)
        self.homegrid = self.get_home_array()
        self.create_node_list(self.grid, self.nodelist)
        self.create_node_list(self.homegrid, self.homelist)
        self.setup_portal_nodes()
        self.move_home_nodes()
        self.homelist[0].is_ghost_start = True

    @staticmethod
    def read_maze_file(txtfile):
        f = open(txtfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    @staticmethod
    def get_home_array():
        return [['0', '0', '+', '0', '0'],
                ['0', '0', '|', '0', '0'],
                ['+', '0', '|', '0', '+'],
                ['+', '-', 'S', '-', '+'],
                ['+', '0', '0', '0', '+']]

    def create_node_list(self, grid, node_list):
        start_node = self.find_first_node(grid)
        self.node_stack.push(start_node)
        while not self.node_stack.is_empty():
            node = self.node_stack.pop()
            self.add_node(node, node_list)

            left_node = self.get_path_node(LEFT, node.row, node.column - 1, node_list, grid)
            right_node = self.get_path_node(RIGHT, node.row, node.column + 1, node_list, grid)
            up_node = self.get_path_node(UP, node.row - 1, node.column, node_list, grid)
            down_node = self.get_path_node(DOWN, node.row + 1, node.column, node_list, grid)

            node.neighbors[LEFT] = left_node
            node.neighbors[RIGHT] = right_node
            node.neighbors[UP] = up_node
            node.neighbors[DOWN] = down_node
            self.add_node_to_stack(left_node, node_list)
            self.add_node_to_stack(right_node, node_list)
            self.add_node_to_stack(up_node, node_list)
            self.add_node_to_stack(down_node, node_list)

    def find_first_node(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] in self.nodeSymbols:
                    node = Node(row, col)
                    if grid[row][col] in self.portalSymbols:
                        node.portal_val = grid[row][col]
                    return node
        return None

    def get_path_node(self, direction, row, col, nodelist, grid):
        temp_node = self.follow_path(direction, row, col, grid)
        return self.get_node_from_node(temp_node, nodelist)

    @staticmethod
    def get_node(x, y, nodelist=None):
        for node in nodelist:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    @staticmethod
    def get_node_from_node(node, nodelist):
        if node is not None:
            for temp_node in nodelist:
                if node.row == temp_node.row and node.column == temp_node.column:
                    return temp_node
        return node

    def add_node(self, node, nodelist):
        node_in_list = self.node_in_list(node, nodelist)
        if not node_in_list:
            nodelist.append(node)

    @staticmethod
    def node_in_list(node, nodelist):
        for inode in nodelist:
            if node.position.x == inode.position.x and node.position.y == inode.position.y:
                return True
        return False

    def follow_path(self, direction, row, col, grid):
        rows = len(grid)
        columns = len(grid[0])
        if direction == LEFT and col >= 0:
            return self.path_to_follow(LEFT, row, col, "-", grid)
        elif direction == RIGHT and col < columns:
            return self.path_to_follow(RIGHT, row, col, "-", grid)
        elif direction == UP and row >= 0:
            return self.path_to_follow(UP, row, col, "|", grid)
        elif direction == DOWN and row < rows:
            return self.path_to_follow(DOWN, row, col, "|", grid)
        else:
            return None

    def path_to_follow(self, direction, row, col, path, grid):
        temp_symbols = [path] + self.nodeSymbols + self.pathSymbols
        if grid[row][col] in temp_symbols:
            while grid[row][col] not in self.nodeSymbols:
                if direction is LEFT:
                    col -= 1
                elif direction is RIGHT:
                    col += 1
                elif direction is UP:
                    row -= 1
                elif direction is DOWN:
                    row += 1
            node = Node(row, col)
            if grid[row][col] == "H":
                node.home_guide = True
            if grid[row][col] == "S":
                node.is_spawn_node = True
            if grid[row][col] == "Y":
                node.is_pacman_start = True
            if grid[row][col] == "F":
                node.is_fruit_start = True
            if grid[row][col] in self.portalSymbols:
                node.portal_val = grid[row][col]
            return node
        else:
            return None

    def move_home_nodes(self):
        node_a = None
        for node in self.nodelist:
            if node.home_guide:
                node_a = node
                break
        node_b = node_a.neighbors[LEFT]
        mid = (node_a.position + node_b.position) / 2.0
        mid = Vector2D(int(mid.x), int(mid.y))
        vec = Vector2D(self.homelist[0].position.x, self.homelist[0].position.y)
        for node in self.homelist:
            node.position -= vec
            node.position += mid
        node_a.neighbors[LEFT] = self.homelist[0]
        node_b.neighbors[RIGHT] = self.homelist[0]
        self.homelist[0].neighbors[RIGHT] = node_a
        self.homelist[0].neighbors[LEFT] = node_b
        self.homelist[0].is_home_entrance = True

    def setup_portal_nodes(self):
        portal_dict = {}
        for i in range(len(self.nodelist)):
            if self.nodelist[i].portal_val != 0:
                if self.nodelist[i].portal_val not in portal_dict.keys():
                    portal_dict[self.nodelist[i].portal_val] = [i]
                else:
                    portal_dict[self.nodelist[i].portal_val] += [i]
        for key in portal_dict.keys():
            node1, node2 = portal_dict[key]
            self.nodelist[node1].portal_node = self.nodelist[node2]
            self.nodelist[node2].portal_node = self.nodelist[node1]

    def add_node_to_stack(self, node, nodelist):
        if node is not None and not self.node_in_list(node, nodelist):
            self.node_stack.push(node)

    def render(self, screen):
        for node in self.nodelist:
            node.render(screen)
        for node in self.homelist:
            node.render(screen)

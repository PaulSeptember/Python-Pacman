import pygame
from constants import*


class Pellet(object):
    def __init__(self, x, y):
        self.name = "pellet"
        self.position = Vector2D(x, y)
        self.color = WHITE
        self.radius = TILE_HEIGHT // 8
        self.points = 10

    def render(self, screen):
        px = int(self.position.x + 8)
        py = int(self.position.y + 8)

        pygame.draw.circle(screen, WHITE2, (px, py), self.radius+2)
        pygame.draw.circle(screen, WHITE1, (px, py), self.radius+1)
        pygame.draw.circle(screen, WHITE, (px, py), self.radius)

    def get_pellet_snapshot(self):
        return self.position.to_tuple() + (self.name,)

class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self, x, y)
        self.name = "powerpellet"
        self.radius = TILE_HEIGHT // 3
        self.points = 50


class PelletGroup(object):
    def __init__(self, mazefile):
        self.pelletList = []
        self.pelletSymbols = ["p", "n" , "Y"]
        self.powerpelletSymbols = ["P", "N"]
        self.create_pellet_list(mazefile)

    @staticmethod
    def read_maze_file(txtfile):
        f = open(txtfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def get_snapshot(self):
        snapshot = []
        for i in self.pelletList:
            snapshot.append(i.get_pellet_snapshot())
        return snapshot

    def create_pellet_list_snap(self,snapshot):
        self.pelletList = []
        for tupl in snapshot:
            if tupl[2] == "powerpellet":
                self.pelletList.append(PowerPellet(tupl[0], tupl[1]))
            if tupl[2] == "pellet":
                self.pelletList.append(Pellet(tupl[0], tupl[1]))


    def create_pellet_list(self, mazefile):
        grid = self.read_maze_file(mazefile)
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] in self.pelletSymbols:
                    self.pelletList.append(Pellet(col * TILE_WIDTH, row * TILE_HEIGHT))
                if grid[row][col] in self.powerpelletSymbols:
                    self.pelletList.append(PowerPellet(col * TILE_WIDTH, row * TILE_HEIGHT))

    def is_empty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)

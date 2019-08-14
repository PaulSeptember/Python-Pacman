from entity import MazeRunner
from constants import *
import random


class Fruit(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "fruit"
        self.color = (0, 200, 0)
        self.set_start_position()
        self.lifespan = 5
        self.timer = 0
        self.set_image()
        self.its_time_to_die = False
        self.points = 200

    def set_image(self):
        sprite_number = random.randint(0, 5)
        self.image = self.spritesheet.get_image(8 + sprite_number % 3, 2 + sprite_number / 3, 32, 32)

    def set_start_position(self):
        self.node = self.find_start_node()
        self.target = self.node.neighbors[LEFT]
        self.set_position()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

    def find_start_node(self):
        for node in self.nodes.nodelist:
            if node.is_fruit_start:
                return node
        return None

    def update(self, dt):
        self.timer += dt
        if self.timer == self.lifespan:
            self.its_time_to_die = True

from entity import MazeRunner
from constants import *
from vectors import Vector2D
from random import randint
from modes import Mode
from stacks import Stack
from animation import Animation, AnimationGroup


# noinspection PyMethodOverriding
# noinspection PyAttributeOutsideInit
class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet, row):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "ghost"
        self.color = PINK
        self.goal = Vector2D()
        self.modeStack = self.setup_mode_stack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0
        self.spawnNode = self.find_spawn_node()
        self.set_guide_stack()
        self.set_start_position()
        self.points = 200
        self.released = True
        self.pelletsForRelease = 0
        self.bannedDirections = []
        self.speed = GHOST_SPEED

        self.animate = AnimationGroup()
        self.animateName = "left"
        self.define_animations(row)
        self.animate.set_animation(self.animateName, 0)
        self.image = self.animate.get_image()
        self.previousDirection = self.direction
        self.started = True
        self.hide = True

    def set_guide_stack(self):
        self.guide = Stack()
        self.guide.push(UP)

    def get_valid_directions(self):
        valid_directions = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if not (key == self.direction * -1):
                    if not self.mode.name == "SPAWN":
                        if not self.node.is_home_entrance:
                            if key not in self.bannedDirections:
                                valid_directions.append(key)
                        else:
                            if key != DOWN:
                                valid_directions.append(key)
                    else:
                        valid_directions.append(key)
        if len(valid_directions) == 0:
            valid_directions.append(self.force_backtrack())
        return valid_directions

    def force_backtrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    def get_closest_direction(self, valid_directions):
        distances = []
        for direction in valid_directions:
            diff_vector = self.node.position + direction * TILE_WIDTH - self.goal
            distances.append(diff_vector.magnitude_squared())
        index = distances.index(min(distances))
        return valid_directions[index]

    def move_by_self(self):
        if self.overshot_target():
            self.node = self.target
            self.portal()
            valid_directions = self.get_valid_directions()
            self.direction = self.get_closest_direction(valid_directions)
            self.target = self.node.neighbors[self.direction]
            self.set_position()
            if self.mode.name == "SPAWN":
                if self.position == self.goal:
                    # self.mode = self.modeStack.pop()
                    self.mode = Mode("GUIDE", speedmult=0.2)
            if self.mode.name == "GUIDE":
                if self.guide.is_empty():
                    self.mode = self.modeStack.pop()
                    self.set_guide_stack()
                    self.started = True
                else:
                    self.direction = self.guide.pop()
                    self.target = self.node.neighbors[self.direction]
                    self.set_position()

    def scatter_goal(self):
        self.goal = Vector2D(SCREENSIZE[0], 0)

    def chase_goal(self, pacman):
        self.goal = pacman.position

    def mode_update(self, dt):
        self.modeTimer += dt

        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    def find_start_node(self):
        for node in self.nodes.homelist:
            if node.is_ghost_start:
                return node
        return None

    def set_start_position(self):
        self.node = self.find_start_node()
        self.target = self.node
        self.set_position()

    def freight_mode(self):
        if self.mode.name != "SPAWN":
            if self.mode.name != "FREIGHT":
                if self.mode.time is not None:
                    dt = self.mode.time - self.modeTimer
                    self.modeStack.push(Mode(name=self.mode.name, time=dt))
                else:
                    self.modeStack.push(Mode(name=self.mode.name))
                self.mode = Mode("FREIGHT", time=7, speedmult=0.5)
                self.modeTimer = 0
                self.animateName = "freight"
                self.animate.set_animation(self.animateName, 0)
            else:
                self.mode = Mode("FREIGHT", time=7, speedmult=0.5)
                self.modeTimer = 0

    def check_direction_change(self):
        if self.direction != self.previousDirection:
            self.previousDirection = self.direction

        if self.mode.name == "SPAWN":
            self.set_spawn_images()
        elif self.mode.name != "FREIGHT":
            self.set_normal_images()

    def spawn_mode(self):
        self.mode = Mode("SPAWN", speedmult=2)
        self.modeTimer = 0
        self.set_spawn_images()

    def random_goal(self):
        x = randint(0, N_COLS * TILE_WIDTH)
        y = randint(0, N_ROWS * TILE_HEIGHT)
        self.goal = Vector2D(x, y)

    def spawn_goal(self):
        self.goal = self.spawnNode.position

    @staticmethod
    def setup_mode_stack():
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    def find_spawn_node(self):
        for node in self.nodes.homelist:
            if node.is_spawn_node:
                return node
        return None

    def set_spawn_images(self):
        if self.started:
            if self.direction == LEFT:
                self.animateName = "spawnleft"
            if self.direction == RIGHT:
                self.animateName = "spawnright"
            if self.direction == UP:
                self.animateName = "spawnup"
            if self.direction == DOWN:
                self.animateName = "spawndown"
            self.animate.set_animation(self.animateName, 0)
        else:
            self.set_normal_images()

    def set_normal_images(self):
        if self.direction == LEFT:
            self.animateName = "left"
        if self.direction == RIGHT:
            self.animateName = "right"
        if self.direction == UP:
            self.animateName = "up"
        if self.direction == DOWN:
            self.animateName = "down"
        self.animate.set_animation(self.animateName, 0)

    def update(self, dt, pacman):
        speed_modifier = self.speed * self.mode.speedmult
        self.position += self.direction * speed_modifier * dt
        self.mode_update(dt)
        self.check_direction_change()
        self.image = self.animate.loop(dt)
        if self.mode.name == "CHASE":
            self.chase_goal(pacman)
        elif self.mode.name == "SCATTER":
            self.scatter_goal()
        elif self.mode.name == "FREIGHT":
            self.random_goal()
        elif self.mode.name == "SPAWN":
            self.spawn_goal()
        self.move_by_self()

    def define_animations(self, row):
        animation = Animation("up")

        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(0, row, 32, 32))
        animation.add_frame(self.spritesheet.get_image(1, row, 32, 32))
        self.animate.add(animation)

        animation = Animation("down")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(2, row, 32, 32))
        animation.add_frame(self.spritesheet.get_image(3, row, 32, 32))
        self.animate.add(animation)

        animation = Animation("left")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(4, row, 32, 32))
        animation.add_frame(self.spritesheet.get_image(5, row, 32, 32))
        self.animate.add(animation)

        animation = Animation("right")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(6, row, 32, 32))
        animation.add_frame(self.spritesheet.get_image(7, row, 32, 32))
        self.animate.add(animation)

        animation = Animation("freight")
        animation.speed = 10
        for i in range(25):
            animation.add_frame(self.spritesheet.get_image(0, 6, 32, 32))
            animation.add_frame(self.spritesheet.get_image(1, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(2, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(3, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(0, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(1, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(2, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(3, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(0, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(1, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(2, 6, 32, 32))
        animation.add_frame(self.spritesheet.get_image(3, 6, 32, 32))
        self.animate.add(animation)

        animation = Animation("spawnup")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(4, 6, 32, 32))
        self.animate.add(animation)

        animation = Animation("spawndown")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(5, 6, 32, 32))
        self.animate.add(animation)

        animation = Animation("spawnleft")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(6, 6, 32, 32))
        self.animate.add(animation)

        animation = Animation("spawnright")
        animation.speed = 10
        animation.add_frame(self.spritesheet.get_image(7, 6, 32, 32))
        self.animate.add(animation)


class Blinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet, 2)
        self.name = "blinky"
        self.color = RED
        self.image = self.spritesheet.get_image(0, 2, 32, 32)

    def set_start_position(self):
        start_node = self.find_start_node()
        self.node = start_node
        self.target = self.node
        self.set_position()


class Pinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet, 3)
        self.name = "pinky"
        self.color = PINK
        self.image = self.spritesheet.get_image(0, 3, 32, 32)

    def scatter_goal(self):
        self.goal = Vector2D()

    def chase_goal(self, pacman):
        self.goal = pacman.position + pacman.direction * TILE_WIDTH * 4

    def set_start_position(self):
        start_node = self.find_start_node()
        self.node = start_node.neighbors[DOWN]
        self.target = self.node
        self.set_position()


class Inky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet, 4)
        self.name = "inky"
        self.color = BLUE
        self.released = False
        self.pelletsForRelease = 30
        self.bannedDirections = [RIGHT]
        self.image = self.spritesheet.get_image(0, 4, 32, 32)

    def scatter_goal(self):
        self.goal = Vector2D()

    def chase_goal(self, pacman):
        self.goal = pacman.position - pacman.direction * TILE_WIDTH * 4

    def set_start_position(self):
        start_node = self.find_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[LEFT]
        self.target = self.node
        self.set_position()


# TODO: original movement pattern
class Clyde(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet, 5)
        self.name = "clyde"
        self.color = ORANGE
        self.released = False
        self.pelletsForRelease = 60
        self.bannedDirections = [LEFT]
        self.image = self.spritesheet.get_image(0, 5, 32, 32)

    def scatter_goal(self):
        self.goal = Vector2D()

    def chase_goal(self, pacman):
        self.goal = pacman.position + pacman.direction * TILE_WIDTH * 4

    def set_start_position(self):
        start_node = self.find_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[RIGHT]
        self.target = self.node
        self.set_position()


class Ghosts(object):
    def __init__(self, nodes, spritesheet):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, spritesheet),
                       Pinky(nodes, spritesheet),
                       Inky(nodes, spritesheet),
                       Clyde(nodes, spritesheet)]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt, pacman):
        for ghost in self.ghosts:
            ghost.update(dt, pacman)

    def freight_mode(self):
        for ghost in self:
            ghost.freight_mode()

    def render(self, screen):
        for ghost in self.ghosts:
            ghost.render(screen)

    def release(self, num_pellets_eaten):
        for ghost in self:
            if not ghost.released:
                if num_pellets_eaten >= ghost.pelletsForRelease:
                    ghost.bannedDirections = []
                    ghost.spawn_mode()
                    ghost.released = True

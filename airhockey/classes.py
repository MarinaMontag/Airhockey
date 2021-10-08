import pygame
import pymunk


class Ball:
    def __init__(self, display, space, player_1, player_2, x=0, y=0, radius=10, velocity=(0, 0), density=1, elasticity=1,
                 collision_type=None, color=(255, 255, 255)):
        self.display = display
        self.space = space
        self.color = color
        self.radius = radius
        self.body = pymunk.Body()
        self.x = x
        self.y = y
        self.velocity = velocity
        self.body.position = (self.x, self.y)
        self.body.velocity = (0, 0)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = density
        self.shape.elasticity = elasticity
        if collision_type is not None:
            self.shape.collision_type = collision_type
        self.space.add(self.body, self.shape)
        self.player_1 = player_1
        self.player_2 = player_2

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(self.display, self.color, (int(x), int(y)), self.radius)

    def to_start_position(self, space, arbiter, data):
        self.body.position = (self.x, self.y)
        self.body.velocity = (0, 0)
        self.player_1.to_start_position()
        self.player_2.to_start_position()
        return False

    def move(self):
        self.body.velocity = self.velocity


class Wall:
    def __init__(self, display, space, start, end, collision_type=None, elasticity=1, thickness=10,
                 color=(255, 255, 255), group=None):
        self.display = display
        self.space = space
        self.color = color
        self.thickness = thickness
        self.start = start
        self.end = end
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, self.start, self.end, self.thickness)
        self.shape.elasticity = elasticity
        self.space.add(self.body, self.shape)
        if collision_type is not None:
            self.shape.collision_type = collision_type
        if group is not None:
            self.shape.filter = pymunk.ShapeFilter(group=group)

    def draw(self):
        pygame.draw.line(self.display, self.color, self.shape.a, self.shape.b, self.thickness)


class Player:
    def __init__(self, display, space, x, offset=30, thickness=10, color=(255, 255, 255), elasticity=1,
                 collision_type=None, group=None):
        self.display = display
        self.space = space
        self.thickness = thickness
        self.color = color
        self.x = x
        self.offset = offset
        middleY = self.display.get_height() / 2
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (self.x, middleY)
        self.start = [0, -offset]
        self.end = [0, offset]
        self.shape = pymunk.Segment(self.body, self.start, self.end, self.thickness)
        self.shape.elasticity = elasticity
        if collision_type is not None:
            self.shape.collision_type = collision_type
        if group is not None:
            self.shape.filter = pymunk.ShapeFilter(group=group)
        self.space.add(self.body, self.shape)

    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(self.display, self.color, p1, p2, self.thickness)

    def move(self, up=True):
        if up:
            self.body.velocity = (0, -600)
        else:
            self.body.velocity = (0, 600)

    def stop(self):
        self.body.velocity = (0, 0)

    def to_start_position(self):
        self.body.position = (self.x, self.display.get_height() / 2)

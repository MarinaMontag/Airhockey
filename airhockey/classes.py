import random
import pygame.gfxdraw
import pygame
import pymunk
from PIL import Image, ImageDraw


class Ball:
    def __init__(self, display, space, left, right, x=0, y=0, radius=10, velocity=None, density=1,
                 elasticity=1, collision_type=None, color=(255, 255, 255)):
        if velocity is None:
            velocity = [0, 0]
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
        self.left = left
        self.right = right

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(self.display, self.color, (int(x), int(y)), self.radius)

    def left_won(self, space, arbiter, data):
        self.to_start_position()
        self.left.score += 1
        print('Left:', self.left.score)
        if self.left.score == self.left.max_score:
            self.left.winner = True
            self.right.winner = False
            print('Winner Left!!!')
        return True

    def right_won(self, space, arbiter, data):
        self.to_start_position()
        self.right.score += 1
        print('Right:', self.right.score)
        if self.right.score == self.right.max_score:
            self.right.winner = True
            self.left.winner = False
            print('Winner Right!!!')
        return True

    def to_start_position(self):
        self.body.position = (self.x, self.y)
        self.body.velocity = (0, 0)
        self.left.to_start_position()
        self.right.to_start_position()

    def move(self):
        self.velocity[0] = self.velocity[0] * random.choice([-1, 1])
        self.velocity[1] = self.velocity[1] * random.choice([-1, 1])
        self.body.velocity = self.velocity


class Wall:
    def __init__(self, display, space, start, end, collision_type=None, elasticity=1, thickness=8,
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
    def __init__(self, display, space, x, radius=30, color=(255, 255, 255), elasticity=1,
                 collision_type=None, group=None, max_score=3, winner=None, velocity=800, arc=(90, -90)):
        self.display = display
        self.space = space
        self.radius = radius
        self.color = color
        self.x = x
        middleY = self.display.get_height() / 2
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (self.x, middleY)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = elasticity
        self.score = 0
        self.max_score = max_score
        self.winner = winner
        self.velocity = velocity
        self.arc = arc
        if collision_type is not None:
            self.shape.collision_type = collision_type
        if group is not None:
            self.shape.filter = pymunk.ShapeFilter(group=group)
        self.space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pil_size = self.radius*2
        pil_image = Image.new("RGBA", (pil_size, pil_size))
        pil_draw = ImageDraw.Draw(pil_image)
        pil_draw.pieslice((0, 0, pil_size-1, pil_size-1), self.arc[0], self.arc[1], fill=self.color)
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        image = pygame.image.fromstring(data, size, mode)
        image_rect = image.get_rect(center=(int(x), int(y)))
        self.display.blit(image, image_rect)

    def move_up(self):
        self.body.velocity = (0, -self.velocity)

    def move_down(self):
        self.body.velocity = (0, self.velocity)

    def play(self, keys, up, down, ball, top, bottom):
        if not self.on_edge(top, bottom):
            if ball.body.velocity != (0, 0):
                if keys[up]:
                    self.move_up()
                elif keys[down]:
                    self.move_down()
                else:
                    self.stop()

    def stop(self):
        self.body.velocity = (0, 0)

    def to_start_position(self):
        self.body.position = (self.x, self.display.get_height() / 2)
        self.stop()

    def on_edge(self, top, bottom):
        if int(self.body.position[1]) <= top:
            self.body.velocity = (0, 0)
            self.body.position = (self.body.position[0], top + self.radius)
        if int(self.body.position[1]) >= bottom:
            self.body.velocity = (0, 0)
            self.body.position = (self.body.position[0], bottom - self.radius)


class Bot(Player):
    def __init__(self, display, space, x, radius=30, color=(255, 255, 255), elasticity=1,
                 collision_type=None, group=None, max_score=3, winner=None, velocity=400, arc=(-90, 90)):
        Player.__init__(self, display, space, x, radius, color, elasticity,
                        collision_type, group, max_score, winner, velocity, arc)

    def bot_play(self, ball, top, bottom):
        self.on_edge(top, bottom)
        bot_y = int(self.body.position[1])
        if ball.body.velocity != (0, 0) and int(ball.body.position[0]) < self.display.get_width() / 2 \
                and ball.body.velocity[0] < 0:
            if int(ball.body.position[1]) < bot_y:
                self.move_up()
            elif int(ball.body.position[1]) > bot_y:
                self.move_down()
            else:
                self.stop()
        else:
            self.going_to_center()

    def going_to_center(self):
        position = int(self.body.position[1])
        center = self.display.get_height() / 2
        if position < center:
            self.move_down()
        elif position > center:
            self.move_up()
        else:
            self.stop()

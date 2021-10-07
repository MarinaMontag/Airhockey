import pygame  # imports the package with all the available pygame modules
import pymunk
from classes import Ball


def pong_game(size=(1000, 600), fps=50, ball_radius=8, velocity=(400, -300)):
    pygame.init()  # initializes each of pygame modules
    display = pygame.display.set_mode(size)
    space = pymunk.Space()  # contains all the information we need in our physics simulation
    clock = pygame.time.Clock()
    left = size[0] / 20
    right = size[0] - left
    top = size[1] / 24
    bottom = size[1] - top
    middleX = size[0] / 2
    middleY = size[1] / 2
    ball = Ball(display, space, x=middleX, y=middleY, radius=ball_radius, velocity=velocity)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((0, 0, 0, 0))
        ball.draw()
        pygame.display.update()
        clock.tick(fps)
        space.step(1 / fps)
    pygame.quit()


if __name__ == '__main__':
    pong_game()

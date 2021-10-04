import pygame  # imports the package with all the available pygame modules
import pymunk

pygame.init()  # initializes each of pygame modules

size = (width, height) = (1000, 600)

display = pygame.display.set_mode(size)

clock = pygame.time.Clock()
fps = 50  # frames per second


def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.update()
        clock.tick(fps)


game()
pygame.quit()

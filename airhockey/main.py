import pygame  # imports the package with all the available pygame modules
import pymunk
from classes import Ball, Wall, Player


def init_game(size):
    pygame.init()  # initializes each of pygame modules
    return pygame.display.set_mode(size), pymunk.Space(), pygame.time.Clock()


def restart_round_if_ended(keys, ball):
    if keys[pygame.K_SPACE] and ball.body.velocity == (0, 0):
        ball.move()


def play(keys, up, down, player):
    if keys[up]:
        player.move()
    elif keys[down]:
        player.move(False)
    else:
        player.stop()


def game_over(player_1, player_2):
    if player_1.winner or player_2.winner:
        pygame.quit()
        return True
    return False


def pong_game(size=(1000, 600), fps=100, ball_radius=8, velocity=(400, -300), goal_left_collision_type=1,
              goal_right_collision_type=2, ball_collision_type=3, offset=20, field_color=(0, 0, 0, 0)):
    display, space, clock = init_game(size)

    left = size[0] / 20
    right = size[0] - left
    top = size[1] / 24
    bottom = size[1] - top
    middleX = size[0] / 2
    middleY = size[1] / 2
    field_height = size[1] - top * 2
    parts = 4
    goal_height = field_height / parts
    goal_top = goal_height * (parts - 1) / 2 + top
    goal_bottom = goal_top + goal_height
    left_player = left + offset
    right_player = right - offset

    player_1 = Player(display, space, left_player)
    player_2 = Player(display, space, right_player)

    ball = Ball(display, space, player_1, player_2, x=middleX, y=middleY, radius=ball_radius, velocity=velocity,
                collision_type=ball_collision_type)

    wall_left_top = Wall(display, space, [left, top], [left, goal_top])
    wall_left_bottom = Wall(display, space, [left, goal_bottom], [left, bottom])
    wall_right_top = Wall(display, space, [right, top], [right, goal_top])
    wall_right_bottom = Wall(display, space, [right, goal_bottom], [right, bottom])
    wall_top = Wall(display, space, [left, top], [right, top])
    wall_bottom = Wall(display, space, [left, bottom], [right, bottom])

    goal_left = Wall(display, space, [left, goal_top], [left, goal_bottom], color=(255, 0, 0),
                     collision_type=goal_left_collision_type)
    goal_right = Wall(display, space, [right, goal_top], [right, goal_bottom], color=(0, 0, 255),
                      collision_type=goal_right_collision_type)

    scored_left = space.add_collision_handler(ball_collision_type, goal_left_collision_type)
    scored_left.begin = ball.right_won

    scored_right = space.add_collision_handler(ball_collision_type, goal_right_collision_type)
    scored_right.begin = ball.left_won

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_over(player_1, player_2):
            return

        keys = pygame.key.get_pressed()

        restart_round_if_ended(keys, ball)

        play(keys, pygame.K_UP, pygame.K_DOWN, player_2)
        play(keys, pygame.K_w, pygame.K_s, player_1)

        display.fill(field_color)
        ball.draw()
        wall_left_top.draw()
        wall_left_bottom.draw()
        wall_right_top.draw()
        wall_right_bottom.draw()
        wall_top.draw()
        wall_bottom.draw()
        goal_left.draw()
        goal_right.draw()
        player_1.draw()
        player_2.draw()

        pygame.display.update()
        clock.tick(fps)
        space.step(1 / fps)


if __name__ == '__main__':
    pong_game()

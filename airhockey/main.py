import pygame  # imports the package with all the available pygame modules
import pymunk
from classes import Ball, Wall, Player


def init_game(size):
    pygame.init()  # initializes each of pygame modules
    return pygame.display.set_mode(size), pymunk.Space(), pygame.time.Clock()


def restart_round_if_ended(keys, ball):
    if keys[pygame.K_SPACE] and ball.body.velocity == (0, 0):
        ball.move()


def play(keys, up, down, player, ball, top, bottom):
    if not player.on_edge(top, bottom):
        if ball.body.velocity != (0, 0):
            if keys[up]:
                player.move()
            elif keys[down]:
                player.move(False)
            else:
                player.stop()


def print_text(display, text, x, y, font_size, bold=True, italic=False, color=(255, 255, 255)):
    font = pygame.font.SysFont('Algerian', font_size, bold, italic)
    surface = font.render(text, True, color)
    display.blit(surface, (x, y))


def pong_game(size=(1000, 600), fps=100, ball_radius=10, velocity=[700, 300], goal_left_collision_type=1,
              goal_right_collision_type=2, ball_collision_type=3, offset=20, field_color=(0, 0, 0, 0),
              player_thickness=12, player_velocity=800, center_line_thickness=4,
              center_line_color=(255, 255, 255, 255)):
    display, space, clock = init_game(size)

    left = size[0] / 40
    right = size[0] - left
    top = size[1] / 17
    bottom = size[1] - top
    middleX = size[0] / 2
    middleY = size[1] / 2
    field_height = size[1] - top * 2
    parts = 4
    goal_height = field_height / parts
    goal_top = goal_height * (parts - 1) / 2 + top
    goal_bottom = goal_top + goal_height
    player_1_pos = left + offset
    player_2_pos = right - offset
    text_score_size = 30
    congrats_text_size = int(size[1]/5)

    player_1 = Player(display, space, player_1_pos, thickness=player_thickness, velocity=player_velocity)
    player_2 = Player(display, space, player_2_pos, thickness=player_thickness, velocity=player_velocity)

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

        display.fill(field_color)
        if not player_1.winner and not player_2.winner:
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
            pygame.draw.line(display, center_line_color, [middleX, top], [middleX, bottom], center_line_thickness)

            print_text(display, f'Score: {player_1.score}', left, 5, text_score_size)
            print_text(display, f'Score: {player_2.score}', right - 100, 5, text_score_size)

            keys = pygame.key.get_pressed()

            play(keys, pygame.K_UP, pygame.K_DOWN, player_2, ball, top, bottom)
            play(keys, pygame.K_w, pygame.K_s, player_1, ball, top, bottom)

            restart_round_if_ended(keys, ball)
        elif player_1.winner:
            print_text(display, 'Winner is Player1', left, int(size[1]/3), congrats_text_size)
        else:
            print_text(display, 'Winner is Player2', left, int(size[1]/3), congrats_text_size)
        pygame.display.update()
        clock.tick(fps)
        space.step(1 / fps)


if __name__ == '__main__':
    pong_game()

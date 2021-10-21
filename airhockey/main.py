import pygame  # imports the package with all the available pygame modules
import pymunk
from classes import *

def restart_round_if_ended(keys, ball):
    if ball.body.velocity == (0, 0) and keys[pygame.K_SPACE]:
        ball.move()


def print_text(display, text, x, y, font_size, bold=True, italic=False, color=(255, 255, 255)):
    font = pygame.font.SysFont('Algerian', font_size, bold, italic)
    surface = font.render(text, True, color)
    display.blit(surface, (x, y))


def pong_game(size=(1000, 600), fps=100, ball_radius=10, ball_velocity=[700, 300], goal_left_collision_type=1,
              goal_right_collision_type=2, ball_collision_type=3, offset=20, field_color=(0, 0, 0, 0),
              player_thickness=12, player_velocity=800, center_line_thickness=4,
              center_line_color=(255, 255, 255, 255)):
    pygame.init()  # initializes each of pygame modules
    display, space, clock = pygame.display.set_mode(size), pymunk.Space(), pygame.time.Clock()

    left_corner_pos = size[0] / 40
    right_corner_pos = size[0] - left_corner_pos
    top_corner_pos = size[1] / 17
    bottom_corner_pos = size[1] - top_corner_pos
    middleX = size[0] / 2
    middleY = size[1] / 2
    field_height = size[1] - top_corner_pos * 2
    parts = 4
    goal_height = field_height / parts
    goal_top = goal_height * (parts - 1) / 2 + top_corner_pos
    goal_bottom = goal_top + goal_height
    bot_pos = left_corner_pos + offset
    player_pos = right_corner_pos - offset
    text_score_size = 30
    congrats_text_size = int(size[1]/5)

    bot = Bot(display, space, bot_pos, thickness=player_thickness, velocity=player_velocity/2)
    player = Player(display, space, player_pos, thickness=player_thickness, velocity=player_velocity)

    ball = Ball(display, space, bot, player, x=middleX, y=middleY, radius=ball_radius, velocity=ball_velocity,
                collision_type=ball_collision_type)

    wall_left_top = Wall(display, space, [left_corner_pos, top_corner_pos], [left_corner_pos, goal_top])
    wall_left_bottom = Wall(display, space, [left_corner_pos, goal_bottom], [left_corner_pos, bottom_corner_pos])
    wall_right_top = Wall(display, space, [right_corner_pos, top_corner_pos], [right_corner_pos, goal_top])
    wall_right_bottom = Wall(display, space, [right_corner_pos, goal_bottom], [right_corner_pos, bottom_corner_pos])
    wall_top = Wall(display, space, [left_corner_pos, top_corner_pos], [right_corner_pos, top_corner_pos])
    wall_bottom = Wall(display, space, [left_corner_pos, bottom_corner_pos], [right_corner_pos, bottom_corner_pos])

    goal_left = Wall(display, space, [left_corner_pos, goal_top], [left_corner_pos, goal_bottom], color=(255, 0, 0),
                     collision_type=goal_left_collision_type)
    goal_right = Wall(display, space, [right_corner_pos, goal_top], [right_corner_pos, goal_bottom], color=(0, 0, 255),
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

        if not bot.winner and not player.winner:
            ball.draw()
            wall_left_top.draw()
            wall_left_bottom.draw()
            wall_right_top.draw()
            wall_right_bottom.draw()
            wall_top.draw()
            wall_bottom.draw()
            goal_left.draw()
            goal_right.draw()
            bot.draw()
            player.draw()

            pygame.draw.line(display, center_line_color, [middleX, top_corner_pos], [middleX, bottom_corner_pos],
                             center_line_thickness)

            print_text(display, f'Score: {bot.score}', left_corner_pos, 5, text_score_size)
            print_text(display, f'Score: {player.score}', right_corner_pos - 100, 5, text_score_size)

            keys = pygame.key.get_pressed()

            bot.bot_play(ball, top_corner_pos, bottom_corner_pos)
            player.play(keys, pygame.K_UP, pygame.K_DOWN, ball, top_corner_pos, bottom_corner_pos)

            restart_round_if_ended(keys, ball)
        elif bot.winner:
            print_text(display, 'Winner is Bot', left_corner_pos, int(size[1]/3), congrats_text_size)
        else:
            print_text(display, 'Winner is Player', left_corner_pos, int(size[1]/3), congrats_text_size)
        pygame.display.update()
        clock.tick(fps)
        space.step(1 / fps)


if __name__ == '__main__':
    pong_game()

import curses
from curses import wrapper
import maze
import numpy
from numpy.random import random_integers as rand
import draw
from player import player


def draw_wall_or_space(x_coord, y_coord, maze_attributes):
    is_wall = str(maze_attributes['walls'][y_coord, x_coord])
    if is_wall == 'True':
        return '#'
    if is_wall == 'False':
        return '.'


# in: finish_game, show_map
# out: running
def main_draw(stdscr, game_state, maze_attributes):
    check_if_player_is_standing_on_exit(game_state, maze_attributes)
    if game_state['finish_game'] is False:
        stdscr.clear()
        if game_state['show_map'] is True:
            draw.draw_with_map(stdscr, game_state, maze_attributes)
        else:
            draw.draw_centered_around_player(stdscr, game_state, maze_attributes)
        stdscr.refresh()
    else:
        stdscr.addstr('YOU WON')
        game_state['running'] = False
        stdscr.getkey()


# curses color pairs init
def colorinit():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)


# in: key, hilite_char, show_map
# out: player_moved, program_running, show_map
def handle_input(key, game_state, maze_attributes, player):
    if (key == 'x'):
        player.stand_still()
        game_state['player_move'] = True
    if (key == 'q'):
        game_state['running'] = False
    if (key == 'f'):
        if game_state['hilite_char'] is False:
            game_state['hilite_char'] = True
        elif game_state['hilite_char'] is True:
            game_state['hilite_char'] = False
    if (key == 'm'):
        if game_state['show_map'] is False:
            game_state['show_map'] = True
        elif game_state['show_map'] is True:
            game_state['show_map'] = False
    if (key == 'w'):
        if game_state['player_position'][0] > 0:
            if draw_wall_or_space(game_state['player_position'][1], game_state['player_position'][0] - 1, maze_attributes) != '#':
                game_state['player_position'][0] -= 1
                game_state['player_move'] = True
    if (key == 's'):
        if game_state['player_position'][0] < maze_attributes['shape'][0]:
            if draw_wall_or_space(game_state['player_position'][1], game_state['player_position'][0] + 1, maze_attributes) != '#':
                game_state['player_position'][0] += 1
                game_state['player_move'] = True
    if (key == 'a'):
        if game_state['player_position'][1] > 0:
            if draw_wall_or_space(game_state['player_position'][1] - 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] -= 1
                game_state['player_move'] = True
    if (key == 'd'):
        if game_state['player_position'][1] < maze_attributes['shape'][1]:
            if draw_wall_or_space(game_state['player_position'][1] + 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] += 1
                game_state['player_move'] = True


# in: player_position
# out:
# in+out: enemy_position
def move_enemy_towards_player(game_state):
    player_x = game_state['player_position'][1]
    player_y = game_state['player_position'][0]
    if game_state['enemy_position'][1] > player_x:
        game_state['enemy_position'][1] -= 1
    if game_state['enemy_position'][1] < player_x:
        game_state['enemy_position'][1] += 1
    if game_state['enemy_position'][0] > player_y:
        game_state['enemy_position'][0] -= 1
    if game_state['enemy_position'][0] < player_y:
        game_state['enemy_position'][0] += 1


# in: walls_location, enemy_pos
def move_enemy_if_standing_on_wall(game_state, maze_attributes):
    while maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]] == 1:
        move_enemy_towards_player(game_state)


def enemy_behaviour_phase_through_walls(game_state, maze_attributes):
    move_enemy_towards_player(game_state)
    move_enemy_if_standing_on_wall(game_state, maze_attributes)
    check_if_player_is_dead(game_state)


def enemy_behaviour_wander_around(game_state, maze_attributes):
    valid_directions = define_valid_directions(game_state, maze_attributes)
    chosen_direction = valid_directions[rand(0, len(valid_directions)-1)]
    if (chosen_direction == 'up'):
        game_state['enemy_position'][0] -= 1
    if (chosen_direction == 'down'):
        game_state['enemy_position'][0] += 1
    if (chosen_direction == 'left'):
        game_state['enemy_position'][1] -= 1
    if (chosen_direction == 'right'):
        game_state['enemy_position'][1] += 1
    check_if_player_is_dead(game_state)


def enemy_behaviour_run_towards_player(game_state, maze_attributes):
    for i in range(2):
        move_enemy_towards_player(game_state)
        check_if_player_is_dead(game_state)


def define_valid_directions(game_state, maze_attributes):
    return_directions = []
    if (maze_attributes['walls'][game_state['enemy_position'][0]-1, game_state['enemy_position'][1]] == 0):
        return_directions.append("up")
    if (maze_attributes['walls'][game_state['enemy_position'][0]+1, game_state['enemy_position'][1]] == 0):
        return_directions.append("down")
    if (maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]-1] == 0):
        return_directions.append("left")
    if (maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]+1] == 0):
        return_directions.append("right")
    return return_directions


def check_direct_line_to_player(game_state, maze_attributes):
    returnvalue = False
    if game_state['player_position'][0] == game_state['enemy_position'][0]:
        i = 0
        while (maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]+i] == 0):
            if (game_state['enemy_position'][1]+i == game_state['player_position'][1]):
                returnvalue = True
            i += 1
        i = 0
        while (maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]+i] == 0):
            if (game_state['enemy_position'][1]+i == game_state['player_position'][1]):
                returnvalue = True
            i -= 1
    if game_state['player_position'][1] == game_state['enemy_position'][1]:
        i = 0
        while (maze_attributes['walls'][game_state['enemy_position'][0]+i, game_state['enemy_position'][1]] == 0):
            if (game_state['enemy_position'][0]+i == game_state['player_position'][0]):
                returnvalue = True
            i += 1
        i = 0
        while (maze_attributes['walls'][game_state['enemy_position'][0]+i, game_state['enemy_position'][1]] == 0):
            if (game_state['enemy_position'][0]+i == game_state['player_position'][0]):
                returnvalue = True
            i -= 1
    return returnvalue


def enemy_move(game_state, maze_attributes):
    player_x = game_state['player_position'][1]
    player_y = game_state['player_position'][0]

    if ((abs(game_state['enemy_position'][1] - player_x) > 13) or
            (abs(game_state['enemy_position'][0] - player_y) > 13)):
        game_state['enemy_behaviour'] = 0
    if ((abs(game_state['enemy_position'][1] - player_x) < 11) and
            (abs(game_state['enemy_position'][0] - player_y) < 11)):
        if ((check_direct_line_to_player(game_state, maze_attributes) is True)):
            game_state['enemy_behaviour'] = 2
        else:
            game_state['enemy_behaviour'] = 1

    if (game_state['enemy_behaviour'] == 0):
        enemy_behaviour_phase_through_walls(game_state, maze_attributes)
    elif (game_state['enemy_behaviour'] == 1):
        enemy_behaviour_wander_around(game_state, maze_attributes)
    elif (game_state['enemy_behaviour'] == 2):
        enemy_behaviour_run_towards_player(game_state, maze_attributes)


def check_if_player_is_dead(game_state):
    if ((abs(game_state['player_position'][0] - game_state['enemy_position'][0]) <= 1) and
            (abs(game_state['player_position'][1] - game_state['enemy_position'][1]) <= 1)):
        game_state['player_dead'] = True


def initialize_game_state():
    game_state = {"running": True, "hilite_char": False,
                  "show_map": False, "finish_game": False, "player_position": [0, 0],
                  "enemy_position": [0, 0], "player_move": False, "enemy_behaviour": 0,
                  "player_dead": False}
    return game_state


def main(stdscr):
    maze_attributes = maze.initialize_maze()
    game_state = initialize_game_state()

    colorinit()
    maze.generate_maze_walls(maze_attributes, game_state)
    set_starting_positions(game_state, maze_attributes)
    
    my_player = player()

    while game_state['running'] is True:
        main_draw(stdscr, game_state, maze_attributes)
        key = stdscr.getkey()
        handle_input(key, game_state, maze_attributes, my_player)
        if game_state['player_move'] is True:
            enemy_move(game_state, maze_attributes)
            game_state['player_move'] = False
        if (game_state['player_dead'] is True):
            main_draw(stdscr, game_state, maze_attributes)
            stdscr.addstr('YOU DIED! GO BACK TO THE ENTRANCE')
            set_starting_positions(game_state, maze_attributes)
            stdscr.getkey()


def check_if_player_is_standing_on_exit(game_state, maze_attributes):
    if ((game_state['player_position'][0] == maze_attributes['exit'][0]) and (
            game_state['player_position'][1] == maze_attributes['exit'][1])):
        game_state['finish_game'] = True


def set_starting_positions(game_state, maze_attributes):
    game_state['player_position'][0] = maze_attributes['entry'][0]
    game_state['player_position'][1] = maze_attributes['entry'][1]

    game_state['enemy_position'] = [0, 0]
    game_state['enemy_behaviour'] = 0

    game_state['player_dead'] = False

    while maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]] == 1:
        game_state['enemy_position'][0] = rand(
            game_state['player_position'][0] + 10, maze_attributes['shape'][0]-1)
        game_state['enemy_position'][1] = rand(
            game_state['player_position'][1] + 10, maze_attributes['shape'][1]-1)


if __name__ == '__main__':
    wrapper(main)

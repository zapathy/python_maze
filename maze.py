import curses
from curses import wrapper
import numpy
from numpy.random import random_integers as rand
import pygame

pygame.init()
pygame.mixer.music.load('slender_foley.wav')
pygame.mixer.music.play(-1)
step = pygame.mixer.Sound('step.wav')
#enemy_vision = pygame.mixer.Sound("slender_2.wav")
#enemy_range = pygame.mixer.Sound('slender_3.wav')


MAZE_ORIGINAL_HEIGHT = 40
MAZE_ORIGINAL_WIDTH = 80
DEBUG_MSG = ""


def getchar2(x, y, maze_attributes):
    retchar = str(maze_attributes['walls'][y, x])
    if retchar == 'True':
        retchar = '#'
    if retchar == 'False':
        retchar = ' '
    return retchar


def draw(stdscr, game_state, maze_attributes):
    checkexit(game_state, maze_attributes)
    if game_state['finish_game'] is False:
        stdscr.clear()
        if game_state['show_map'] is True:
            for y in range(maze_attributes['shape'][0]):
                for x in range(maze_attributes['shape'][1]):
                    if ((y == game_state['player_position'][0]) and (
                            x == game_state['player_position'][1])):
                        if game_state['player_dead'] is False:
                            stdscr.addstr('@', curses.color_pair(1))
                        else:
                            stdscr.addstr('@', curses.color_pair(6))
                    else:
                        if ((y == game_state['enemy_position'][0]) and (x == game_state['enemy_position'][1])):
                            if game_state['enemy_behaviour'] == 2:
                                stdscr.addstr('&', curses.color_pair(6))
                            else:
                                stdscr.addstr('&', curses.color_pair(1))
                        else:
                            if ((y == maze_attributes['entry'][0]) and (x == maze_attributes['entry'][1])):
                                stdscr.addstr('*', curses.color_pair(2))
                            else:
                                if ((y == maze_attributes['exit'][0]) and (
                                        x == maze_attributes['exit'][1])):
                                    stdscr.addstr('$', curses.color_pair(3))
                                else:
                                    cchar = getchar2(x, y, maze_attributes)
                                    if ((game_state['hilite_char'] is True) and (
                                            (x == game_state['player_position'][1]) or
                                            (y == game_state['player_position'][0]))):
                                        stdscr.addstr(
                                            cchar, curses.color_pair(5))
                                    else:
                                        stdscr.addstr(
                                            cchar, curses.color_pair(4))
                stdscr.addstr('\n')
        else:
            max = 4
            y = max * (-1)
            while y <= max:
                drawnline = False
                x = max * (-1)
                while x <= max:
                    if ((game_state['player_position'][1] + x < 0) or
                            (game_state['player_position'][1] + x > maze_attributes['shape'][1] - 1) or (
                            game_state['player_position'][0] + y < 0) or
                            (game_state['player_position'][0] + y > maze_attributes['shape'][0] - 1)):
                        pass
                    else:
                        drawnline = True
                        if ((x == 0) and (y == 0)):
                            if game_state['player_dead'] is False:
                                stdscr.addstr('@', curses.color_pair(1))
                            else:
                                stdscr.addstr('@', curses.color_pair(6))
                        else:
                            if ((game_state['player_position'][1] + x == game_state['enemy_position'][1])
                                    and (game_state['player_position'][0] + y == game_state['enemy_position'][0])):
                                if game_state['enemy_behaviour'] == 2:
                                    stdscr.addstr('&', curses.color_pair(6))
                                else:
                                    stdscr.addstr('&', curses.color_pair(1))
                            else:
                                if ((game_state['player_position'][1] + x == maze_attributes['entry'][1])
                                        and (game_state['player_position'][0] + y == maze_attributes['entry'][0])):
                                    stdscr.addstr('*', curses.color_pair(2))
                                else:
                                    if ((game_state['player_position'][1] + x == maze_attributes['exit'][1])
                                            and (game_state['player_position'][0] + y) == maze_attributes['exit'][0]):
                                        stdscr.addstr(
                                            '$', curses.color_pair(3))
                                    else:
                                        cchar = getchar2(
                                            game_state['player_position'][1] +
                                            x, game_state['player_position'][0] + y,
                                            maze_attributes)
                                        if (game_state['hilite_char'] is True):
                                            stdscr.addstr(
                                                cchar, curses.color_pair(5))
                                        else:
                                            stdscr.addstr(
                                                cchar, curses.color_pair(4))
                    x += 1
                y += 1
                if (drawnline is True):
                    stdscr.addstr('\n')
                    drawnline = False
                game_state['hilite_char'] = False
        stdscr.refresh()
    else:
        stdscr.addstr('YOU WON')
        game_state['running'] = False
        stdscr.getkey()


def colorinit():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)


def input(key, game_state, maze_attributes):
    if (key == 'x'):
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
        pygame.mixer.Sound.play(step)
        if game_state['player_position'][0] > 0:
            if getchar2(game_state['player_position'][1], game_state['player_position'][0] - 1, maze_attributes) != '#':
                game_state['player_position'][0] -= 1
                game_state['player_move'] = True
    if (key == 's'):
        pygame.mixer.Sound.play(step)
        if game_state['player_position'][0] < maze_attributes['shape'][0]:
            if getchar2(game_state['player_position'][1], game_state['player_position'][0] + 1, maze_attributes) != '#':
                game_state['player_position'][0] += 1
                game_state['player_move'] = True
    if (key == 'a'):
        pygame.mixer.Sound.play(step)
        if game_state['player_position'][1] > 0:
            if getchar2(game_state['player_position'][1] - 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] -= 1
                game_state['player_move'] = True
    if (key == 'd'):
        pygame.mixer.Sound.play(step)
        if game_state['player_position'][1] < maze_attributes['shape'][1]:
            if getchar2(game_state['player_position'][1] + 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] += 1
                game_state['player_move'] = True


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


def move_enemy_through_wall(game_state, maze_attributes):
    while maze_attributes['walls'][game_state['enemy_position'][0], game_state['enemy_position'][1]] == 1:
        move_enemy_towards_player(game_state)


def enemy_movement_behaviour_type_0(game_state, maze_attributes):
    move_enemy_towards_player(game_state)
    move_enemy_through_wall(game_state, maze_attributes)
    check_player_death(game_state)


def enemy_movement_behaviour_type_1(game_state, maze_attributes):
    valid_directions = define_valid_directions(game_state, maze_attributes)
    actual_direction = valid_directions[rand(0, len(valid_directions)-1)]
    if (actual_direction == 'up'):
        game_state['enemy_position'][0] -= 1
    if (actual_direction == 'down'):
        game_state['enemy_position'][0] += 1
    if (actual_direction == 'left'):
        game_state['enemy_position'][1] -= 1
    if (actual_direction == 'right'):
        game_state['enemy_position'][1] += 1
    check_player_death(game_state)


def enemy_movement_behaviour_type_2(game_state, maze_attributes):
    for i in range(2):
        move_enemy_towards_player(game_state)
        check_player_death(game_state)


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

    if ((abs(game_state['enemy_position'][1] - player_x) > 11) or
    (abs(game_state['enemy_position'][0] - player_y) > 11)):
        game_state['enemy_behaviour'] = 0
    if ((abs(game_state['enemy_position'][1] - player_x) < 13) and
    (abs(game_state['enemy_position'][0] - player_y) < 13)):
        if ((check_direct_line_to_player(game_state, maze_attributes) is True)):
            game_state['enemy_behaviour'] = 2
        else:
            game_state['enemy_behaviour'] = 1

    if (game_state['enemy_behaviour'] == 0):
        enemy_movement_behaviour_type_0(game_state, maze_attributes)
        #pygame.mixer.Sound.play(music, loops=-1 )
    elif (game_state['enemy_behaviour'] == 1):
        enemy_movement_behaviour_type_1(game_state, maze_attributes)
        #pygame.mixer.Sound.play(enemy_vision, loops=-1 )
    elif (game_state['enemy_behaviour'] == 2):
        enemy_movement_behaviour_type_2(game_state, maze_attributes)
        #pygame.mixer.Sound.play(enemy_range, loops=-1 )



def check_player_death(game_state):
    if ((abs(game_state['player_position'][0] - game_state['enemy_position'][0]) <= 1) and
            (abs(game_state['player_position'][1] - game_state['enemy_position'][1]) <= 1)):
        game_state['player_dead'] = True


def main(stdscr):
    maze_attributes = {'entry': [
        0, 0]}
    maze_attributes['shape'] = (
        (MAZE_ORIGINAL_HEIGHT // 2) * 2 + 1, (MAZE_ORIGINAL_WIDTH // 2) * 2 + 1)
    maze_attributes['exit'] = [0, 0]
    maze_attributes['walls'] = numpy.zeros(
        maze_attributes['shape'], dtype=bool)

    game_state = {"running": True, "hilite_char": False,
                  "show_map": False, "finish_game": False, "player_position": [0, 0],
                  "enemy_position": [0, 0], "player_move": False, "enemy_behaviour": 0,
                  "player_dead": False}
    colorinit()
    maze(maze_attributes, game_state)
    while game_state['running'] is True:
        draw(stdscr, game_state, maze_attributes)
        global DEBUG_MSG
        stdscr.addstr(DEBUG_MSG)
        DEBUG_MSG = ""
        key = stdscr.getkey()
        input(key, game_state, maze_attributes)
        if game_state['player_move'] is True:
            enemy_move(game_state, maze_attributes)
            game_state['player_move'] = False
        if (game_state['player_dead'] is True):
            draw(stdscr, game_state, maze_attributes)
            stdscr.addstr('YOU DIED! GO BACK TO THE ENTRANCE')
            set_starting_positions(game_state, maze_attributes)
            stdscr.getkey()


def checkexit(game_state, maze_attributes):
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


def maze(maze_attributes, game_state):

    complexity = .85
    density = .85
    # Only odd shapes
    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(
        complexity * (5 * (maze_attributes['shape'][0] + maze_attributes['shape'][1])))
    # size of components
    density = int(
        density * ((maze_attributes['shape'][0] // 2) * (maze_attributes['shape'][1] // 2)))
    # Build actual maze

    # Fill borders
    maze_attributes['walls'][0, :] = maze_attributes['walls'][-1, :] = 1
    maze_attributes['walls'][:, 0] = maze_attributes['walls'][:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, maze_attributes['shape'][1] // 2) * 2, rand(0,
                                                                   maze_attributes['shape'][0] // 2) * 2
        # pick a random position
        maze_attributes['walls'][y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < maze_attributes['shape'][1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < maze_attributes['shape'][0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand(0, len(neighbours) - 1)]
                if maze_attributes['walls'][y_, x_] == 0:
                    maze_attributes['walls'][y_, x_] = 1
                    maze_attributes['walls'][y_ +
                                             (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    maze_attributes['entry'] = [0, 1]
    maze_attributes['exit'] = [maze_attributes['shape']
                               [0] // 2, maze_attributes['shape'][1] // 2]

    maze_attributes['walls'][maze_attributes['entry']
                             [0], maze_attributes['entry'][1]] = 0
    maze_attributes['walls'][maze_attributes['exit']
                             [0], maze_attributes['exit'][1]] = 0

    set_starting_positions(game_state, maze_attributes)

    return maze_attributes['walls']


wrapper(main)

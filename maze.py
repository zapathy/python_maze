import curses
from curses import wrapper
import numpy
from numpy.random import random_integers as rand


MAZE_ORIGINAL_HEIGHT = 40
MAZE_ORIGINAL_WIDTH = 80


def getchar2(x, y, maze_attributes):
    retchar = str(maze_attributes['walls'][y, x])
    if retchar == 'True':
        retchar = '#'
    if retchar == 'False':
        retchar = '.'
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
                        stdscr.addstr('@', curses.color_pair(1))
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
                                        (x == game_state['player_position'][1]) or (y == game_state['player_position'][0]))):
                                    stdscr.addstr(cchar, curses.color_pair(5))
                                else:
                                    stdscr.addstr(cchar, curses.color_pair(4))
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
                            stdscr.addstr('@', curses.color_pair(1))
                        else:
                            if ((game_state['player_position'][1] + x == maze_attributes['entry'][1])
                                    and (game_state['player_position'][0] + y) == maze_attributes['entry'][0]):
                                stdscr.addstr('*', curses.color_pair(2))
                            else:
                                if ((game_state['player_position'][1] + x == maze_attributes['exit'][1])
                                        and (game_state['player_position'][0] + y) == maze_attributes['exit'][0]):
                                    stdscr.addstr('$', curses.color_pair(3))
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


def input(key, game_state, maze_attributes):
    if (key == 'q'):
        game_state['running'] = False
    if (key == 'f'):
        game_state['hilite_char'] = True
    if (key == 'm'):
        if game_state['show_map'] is False:
            game_state['show_map'] = True
        elif game_state['show_map'] is True:
            game_state['show_map'] = False
    if (key == 'w'):
        if game_state['player_position'][0] > 0:
            if getchar2(game_state['player_position'][1], game_state['player_position'][0] - 1, maze_attributes) != '#':
                game_state['player_position'][0] -= 1
    if (key == 's'):
        if game_state['player_position'][0] < maze_attributes['shape'][0]:
            if getchar2(game_state['player_position'][1], game_state['player_position'][0] + 1, maze_attributes) != '#':
                game_state['player_position'][0] += 1
    if (key == 'a'):
        if game_state['player_position'][1] > 0:
            if getchar2(game_state['player_position'][1] - 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] -= 1
    if (key == 'd'):
        if game_state['player_position'][1] < maze_attributes['shape'][1]:
            if getchar2(game_state['player_position'][1] + 1, game_state['player_position'][0], maze_attributes) != '#':
                game_state['player_position'][1] += 1


def main(stdscr):

    maze_attributes = {'entry': [
        0, 0]}
    maze_attributes['shape'] = (
        (MAZE_ORIGINAL_HEIGHT // 2) * 2 + 1, (MAZE_ORIGINAL_WIDTH // 2) * 2 + 1)
    maze_attributes['exit'] = [0, 0]
    maze_attributes['walls'] = numpy.zeros(
        maze_attributes['shape'], dtype=bool)

    game_state = {"running": True, "hilite_char": False,
                  "show_map": False, "finish_game": False, "player_position": [0, 0]}
    colorinit()
    maze(maze_attributes, game_state)
    while game_state['running'] is True:
        draw(stdscr, game_state, maze_attributes)
        key = stdscr.getkey()
        input(key, game_state, maze_attributes)


def checkexit(game_state, maze_attributes):
    if ((game_state['player_position'][0] == maze_attributes['exit'][0]) and (
            game_state['player_position'][1] == maze_attributes['exit'][1])):
        game_state['finish_game'] = True


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
    game_state['player_position'][0] = maze_attributes['entry'][0]
    game_state['player_position'][1] = maze_attributes['entry'][1]

    return maze_attributes['walls']


wrapper(main)
